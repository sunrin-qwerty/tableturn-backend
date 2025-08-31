import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from tortoise import Tortoise
from app.common.utils.env_validator import settings
from app.members.entities.member import MemberEntity


def clean_input_string(text: str) -> str:
    """입력 문자열을 UTF-8로 안전하게 정리하는 함수"""
    try:
        # 문자열을 UTF-8로 인코딩했다가 다시 디코딩하여 잘못된 문자 제거
        return text.encode("utf-8", errors="ignore").decode("utf-8")
    except Exception:
        # 만약 그래도 문제가 있다면 ASCII 문자만 남기기
        return "".join(char for char in text if ord(char) < 128)


async def create_custom_admin_member(
    nickname: str, email: str, profile_url: str = None
):
    """사용자 정의 관리자 멤버를 생성하는 함수"""

    # 입력값들을 안전하게 정리
    nickname = clean_input_string(nickname)
    email = clean_input_string(email)
    if profile_url:
        profile_url = clean_input_string(profile_url)

    print(f"정리된 입력값 - 닉네임: {repr(nickname)}, 이메일: {repr(email)}")

    # 데이터베이스 연결 초기화
    await Tortoise.init(
        config={
            "connections": {
                "default": settings.DATABASE_URI,
            },
            "apps": {
                "models": {
                    "models": ["app.members.entities"],
                    "default_connection": "default",
                },
            },
        }
    )

    try:
        # 이메일 중복 확인
        existing_member = await MemberEntity.filter(email=email).first()

        if existing_member:
            print(f"해당 이메일로 이미 계정이 존재합니다: {email}")

            # 기존 계정을 관리자로 업그레이드
            if not existing_member.is_admin:
                existing_member.is_admin = True
                await existing_member.save()
                print(f"기존 계정을 관리자로 업그레이드했습니다: {email}")

            return existing_member

        # 새로운 관리자 계정 생성
        admin_data = {
            "nickname": nickname,
            "email": email,
            "profile_url": profile_url,
            "is_admin": True,
        }

        admin_member = await MemberEntity.create(**admin_data)

        print(f"사용자 정의 관리자 계정이 성공적으로 생성되었습니다!")
        print(f"ID: {admin_member.id}")
        print(f"닉네임: {admin_member.nickname}")
        print(f"이메일: {admin_member.email}")
        print(f"관리자 권한: {admin_member.is_admin}")

        return admin_member

    except Exception as e:
        print(f"관리자 계정 생성 중 오류가 발생했습니다: {e}")
        raise e

    finally:
        # 데이터베이스 연결 종료
        await Tortoise.close_connections()


def safe_input(prompt: str) -> str:
    """안전한 입력을 받는 함수"""
    try:
        # 터미널 인코딩을 명시적으로 설정
        import locale

        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    except:
        pass

    while True:
        try:
            text = input(prompt).strip()
            # 입력받은 텍스트를 UTF-8로 검증
            text.encode("utf-8")
            return text
        except UnicodeEncodeError:
            print("입력에 잘못된 문자가 포함되어 있습니다. 다시 입력해주세요.")
        except UnicodeDecodeError:
            print("입력에 잘못된 문자가 포함되어 있습니다. 다시 입력해주세요.")
        except Exception as e:
            print(f"입력 오류: {e}. 다시 입력해주세요.")


async def main():
    """메인 실행 함수"""
    print("=== 관리자 계정 생성 ===")

    # 안전한 입력 받기
    nickname = safe_input("닉네임을 입력하세요: ")
    email = safe_input("이메일을 입력하세요: ")
    profile_url_input = safe_input(
        "프로필 URL을 입력하세요 (선택 사항, 엔터로 건너뛰기): "
    )
    profile_url = profile_url_input if profile_url_input else None

    # 기본 관리자 계정 생성
    await create_custom_admin_member(
        nickname=nickname, email=email, profile_url=profile_url
    )


if __name__ == "__main__":
    asyncio.run(main())
