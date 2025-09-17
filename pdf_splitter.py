#!/usr/bin/env python3
"""
PDF 파일을 100페이지씩 분할하는 프로그램
PyPDF2 라이브러리를 사용하여 PDF 파일을 분할합니다.
"""

import os
import sys
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def split_pdf(input_path, pages_per_split=100):
    """
    PDF 파일을 지정된 페이지 수씩 분할합니다.
    
    Args:
        input_path (str): 입력 PDF 파일 경로
        pages_per_split (int): 각 분할 파일의 페이지 수 (기본값: 100)
    
    Returns:
        list: 생성된 파일 경로들의 리스트
    """
    try:
        # PDF 파일 읽기
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        print(f"총 페이지 수: {total_pages}")
        print(f"분할 단위: {pages_per_split}페이지")
        
        # 입력 파일명에서 확장자 제거
        input_file = Path(input_path)
        base_name = input_file.stem
        output_dir = input_file.parent / f"{base_name}_split"
        
        # 출력 디렉토리 생성
        output_dir.mkdir(exist_ok=True)
        
        created_files = []
        
        # 페이지별로 분할
        for start_page in range(0, total_pages, pages_per_split):
            end_page = min(start_page + pages_per_split, total_pages)
            
            # 새로운 PDF 작성자 생성
            writer = PdfWriter()
            
            # 해당 페이지 범위의 페이지들을 추가
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # 출력 파일명 생성
            output_filename = f"{base_name}_part_{start_page//pages_per_split + 1:03d}.pdf"
            output_path = output_dir / output_filename
            
            # PDF 파일 저장
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            created_files.append(str(output_path))
            print(f"생성됨: {output_filename} (페이지 {start_page+1}-{end_page})")
        
        print(f"\n총 {len(created_files)}개의 파일이 생성되었습니다.")
        print(f"출력 디렉토리: {output_dir}")
        
        return created_files
        
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {input_path}")
        return []
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return []


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python pdf_splitter.py <PDF파일경로> [페이지수]")
        print("예시: python pdf_splitter.py document.pdf 100")
        print("예시: python pdf_splitter.py document.pdf 50")
        return
    
    input_path = sys.argv[1]
    pages_per_split = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    # 파일 존재 확인
    if not os.path.exists(input_path):
        print(f"오류: 파일이 존재하지 않습니다 - {input_path}")
        return
    
    # PDF 파일인지 확인
    if not input_path.lower().endswith('.pdf'):
        print("오류: PDF 파일이 아닙니다.")
        return
    
    print(f"PDF 분할 시작: {input_path}")
    print(f"분할 단위: {pages_per_split}페이지")
    print("-" * 50)
    
    # PDF 분할 실행
    created_files = split_pdf(input_path, pages_per_split)
    
    if created_files:
        print("\n분할 완료!")
    else:
        print("\n분할 실패!")


if __name__ == "__main__":
    main()



