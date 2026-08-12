#!/usr/bin/env python3
"""SilverLink 본선 발표 PPT 생성 스크립트"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml
import os

# 색상 정의
BLUE_PRIMARY = RgbColor(0x1E, 0x88, 0xE5)  # #1E88E5
BLUE_DARK = RgbColor(0x0D, 0x47, 0xA1)     # #0D47A1
GRAY_DARK = RgbColor(0x33, 0x33, 0x33)     # #333333
GRAY_LIGHT = RgbColor(0x66, 0x66, 0x66)    # #666666
WHITE = RgbColor(0xFF, 0xFF, 0xFF)
CORAL = RgbColor(0xFF, 0x6B, 0x6B)         # #FF6B6B

# 프레젠테이션 생성 (16:9)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_gradient_background(slide, color1, color2):
    """그라데이션 배경 추가 (간단한 단색으로 대체)"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color1

def add_title_slide(prs, title, subtitle, is_first=False):
    """타이틀 슬라이드 추가"""
    slide_layout = prs.slide_layouts[6]  # 빈 슬라이드
    slide = prs.slides.add_slide(slide_layout)

    # 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BLUE_PRIMARY

    # 로고 추가 (첫 슬라이드만)
    if is_first:
        logo_path = "docs/hackathon/silverlink_logo_horizontal.png"
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(4.2), Inches(1.5), width=Inches(5))

    # 타이틀
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(12.333), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # 서브타이틀
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(5), Inches(12.333), Inches(1))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(28)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    return slide

def add_content_slide(prs, title, bullets, note=""):
    """내용 슬라이드 추가"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 흰 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE

    # 상단 컬러 바
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE_PRIMARY
    shape.line.fill.background()

    # 타이틀
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    # 불릿 포인트
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(12), Inches(5))
    tf = content_box.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {bullet}"
        p.font.size = Pt(28)
        p.font.color.rgb = GRAY_DARK
        p.space_after = Pt(20)

    # 노트 (발표자용)
    if note:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note

    return slide

def add_video_slide(prs):
    """영상 재생 슬라이드"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 검은 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RgbColor(0x1A, 0x1A, 0x2E)

    # 메인 텍스트
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "시연 영상"
    p.font.size = Pt(60)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # 서브 텍스트
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(12.333), Inches(1))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = "aiconic_demo_final.mp4 (3분 11초)"
    p.font.size = Pt(24)
    p.font.color.rgb = RgbColor(0xBB, 0xBB, 0xBB)
    p.alignment = PP_ALIGN.CENTER

    # 재생 아이콘 (삼각형으로 대체)
    play_icon = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(6.2), Inches(5.2), Inches(1), Inches(0.8))
    play_icon.rotation = 90
    play_icon.fill.solid()
    play_icon.fill.fore_color.rgb = WHITE
    play_icon.line.fill.background()

    # 노트
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = """[영상 재생 - 3분 11초]
파일: aiconic_demo_final.mp4

영상 재생 전 멘트:
"지금부터 SilverLink가 실제로 어떻게 작동하는지 보여드리겠습니다."

영상 종료 후 멘트:
"보신 것처럼, 버튼 하나로 30초 만에 맞춤 복지 혜택을 찾을 수 있습니다."
"""

    return slide

def add_differentiation_slide(prs):
    """차별화 포인트 슬라이드 (3열)"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 흰 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE

    # 상단 바
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE_PRIMARY
    shape.line.fill.background()

    # 타이틀
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "차별화 포인트"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    # 3개 박스
    items = [
        ("실시간 녹음", "파일 업로드 없이\n버튼 하나로 즉시 녹음", "01"),
        ("완전 무료", "Gemini API 단독 사용\n월 60만원 비용 절감", "02"),
        ("할루시네이션 방지", "20개 검증된 데이터\n기반 추천만 제공", "03"),
    ]

    for i, (title, desc, num) in enumerate(items):
        x = Inches(0.8 + i * 4.1)

        # 박스 배경
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2), Inches(3.8), Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = RgbColor(0xF5, 0xF5, 0xF5)
        box.line.fill.background()

        # 번호
        num_box = slide.shapes.add_textbox(x + Inches(0.2), Inches(2.2), Inches(1), Inches(0.8))
        tf = num_box.text_frame
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = BLUE_PRIMARY

        # 타이틀
        t_box = slide.shapes.add_textbox(x + Inches(0.2), Inches(3), Inches(3.4), Inches(0.8))
        tf = t_box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = GRAY_DARK

        # 설명
        d_box = slide.shapes.add_textbox(x + Inches(0.2), Inches(3.8), Inches(3.4), Inches(2))
        tf = d_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(20)
        p.font.color.rgb = GRAY_LIGHT

    return slide

def add_tech_slide(prs):
    """기술 스택 슬라이드"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 흰 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE

    # 상단 바
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE_PRIMARY
    shape.line.fill.background()

    # 타이틀
    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "기술 스택 & 향후 발전 방안"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK

    # 왼쪽: 기술 스택
    left_title = slide.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(5.5), Inches(0.6))
    tf = left_title.text_frame
    p = tf.paragraphs[0]
    p.text = "현재 기술 스택"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY

    tech_items = [
        "Frontend: Streamlit (Python)",
        "AI: Google Gemini 2.0 Flash",
        "TTS: gTTS (무료)",
        "Deploy: Streamlit Cloud",
        "Data: 20개 복지 혜택 JSON"
    ]

    left_content = slide.shapes.add_textbox(Inches(0.7), Inches(2.4), Inches(5.5), Inches(4))
    tf = left_content.text_frame
    tf.word_wrap = True
    for i, item in enumerate(tech_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(22)
        p.font.color.rgb = GRAY_DARK
        p.space_after = Pt(12)

    # 오른쪽: 향후 발전
    right_title = slide.shapes.add_textbox(Inches(7), Inches(1.7), Inches(5.5), Inches(0.6))
    tf = right_title.text_frame
    p = tf.paragraphs[0]
    p.text = "향후 발전 방안"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = CORAL

    future_items = [
        "복지로 Open API 연동",
        "지역별 복지 정보 확대",
        "지자체/복지관 연계",
        "음성 UX 고도화",
        "다국어 지원 (다문화 가정)"
    ]

    right_content = slide.shapes.add_textbox(Inches(7), Inches(2.4), Inches(5.5), Inches(4))
    tf = right_content.text_frame
    tf.word_wrap = True
    for i, item in enumerate(future_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(22)
        p.font.color.rgb = GRAY_DARK
        p.space_after = Pt(12)

    return slide

def add_closing_slide(prs):
    """마무리 슬라이드 (QR 코드)"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 배경
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BLUE_PRIMARY

    # 메인 메시지
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1), Inches(12.333), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "기술이 복지 사각지대를 없앨 수 있습니다"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # QR 코드 이미지
    qr_path = "slides/qr_code.png"
    if os.path.exists(qr_path):
        slide.shapes.add_picture(qr_path, Inches(5.4), Inches(2.5), width=Inches(2.5))
    else:
        # QR 코드 없으면 placeholder
        qr_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.4), Inches(2.5), Inches(2.5), Inches(2.5))
        qr_box.fill.solid()
        qr_box.fill.fore_color.rgb = WHITE

    # URL
    url_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(12.333), Inches(0.6))
    tf = url_box.text_frame
    p = tf.paragraphs[0]
    p.text = "silverlink-ai-welfare-6kn44w2jypeuce5d9zrsfg.streamlit.app"
    p.font.size = Pt(18)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # CTA
    cta_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.8), Inches(12.333), Inches(0.6))
    tf = cta_box.text_frame
    p = tf.paragraphs[0]
    p.text = "지금 바로 체험해보세요!"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # 감사합니다
    thanks_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(12.333), Inches(0.8))
    tf = thanks_box.text_frame
    p = tf.paragraphs[0]
    p.text = "감사합니다"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    return slide


# === 슬라이드 생성 ===

# 1. 타이틀
add_title_slide(prs, "", "AI-conic 해커톤 본선 발표 | 팀: 이상재 (1인 개발)", is_first=True)

# 2. 문제 정의
add_content_slide(prs,
    "문제 정의",
    [
        "복지 혜택 미신청률 30% - 연간 수조원 미집행",
        "복잡한 신청 절차 → 어르신들의 포기",
        "디지털 격차로 인한 복지 사각지대 심화",
        "\"어떤 복지를 받을 수 있는지조차 모른다\""
    ],
    note="[50초] 문제 공감대 형성\n\n멘트: \"대한민국에서 매년 수조원의 복지 예산이 집행되지 못합니다. 이유는 단 하나, 신청 방법이 너무 복잡하기 때문입니다.\""
)

# 3. 솔루션
add_content_slide(prs,
    "솔루션: SilverLink",
    [
        "어르신이 \"말로\" 상황을 설명하면",
        "AI가 즉시 받을 수 있는 복지 혜택을 추천",
        "버튼 하나로 시작 → 30초 만에 결과 확인",
        "복잡한 절차 없이, 파일 업로드 없이"
    ],
    note="[40초] 솔루션 핵심 가치\n\n멘트: \"SilverLink는 어르신들이 '그냥 말로' 상황을 설명하면, AI가 즉시 받을 수 있는 복지 혜택을 알려드립니다.\""
)

# 4. 시연 영상
add_video_slide(prs)

# 5. 차별화 포인트
add_differentiation_slide(prs)

# 6. 기술 스택 + 향후 발전
add_tech_slide(prs)

# 7. 마무리
add_closing_slide(prs)

# 저장
output_path = "SilverLink_본선발표.pptx"
prs.save(output_path)
print(f"✅ PPT 생성 완료: {output_path}")
print(f"   - 총 {len(prs.slides)}개 슬라이드")
print(f"   - 16:9 비율")
print(f"\n📁 파일 위치: {os.path.abspath(output_path)}")
