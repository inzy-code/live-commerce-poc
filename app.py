import streamlit as st
import json
import re
import time
from datetime import datetime
from collections import Counter

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN HIỆN ĐẠI & TƯƠI SÁNG (LIGHT & CLEAN THEME)
# ==============================================================================
st.set_page_config(
    page_title="Bàn Điều Hành Trợ Lý Livestream",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS giao diện Sáng, Tối Giản, Dễ Sử Dụng
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1e293b;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.2rem;
    }

    /* Header phong cách Sáng, Sang Trọng */
    .light-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 50%, #eef2ff 100%);
        border: 1px solid #e0e7ff;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.06);
    }
    .light-header h1 {
        margin: 0;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.4px;
        color: #1e1b4b !important;
    }
    .light-header p {
        margin: 4px 0 0 0;
        font-size: 0.9rem;
        color: #64748b;
    }

    /* Huy hiệu trạng thái mềm mại */
    .pill-live {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .pill-ready {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Thẻ cảnh báo khiếu nại (Thân thiện, rõ ràng, không u ám) */
    .complaint-card {
        background-color: #fff1f2;
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 16px;
    }
    .complaint-title {
        color: #991b1b;
        font-weight: 700;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .complaint-body {
        color: #7f1d1d;
        font-size: 0.85rem;
        margin-top: 3px;
        line-height: 1.45;
    }

    /* Thẻ gợi ý Ghim Deal (Tươi sáng, bắt mắt) */
    .deal-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #fee2e2 100%);
        border: 1.5px solid #fbbf24;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.12);
    }
    .deal-badge {
        background-color: #ea580c;
        color: white;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 9999px;
        letter-spacing: 0.3px;
    }

    /* Khung hiển thị bảo mật thông tin PII */
    .mask-preview-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 0.86rem;
        line-height: 1.5;
        color: #334155;
    }

    /* Khung điện thoại Live Stream Shopper View */
    .phone-mockup {
        max-width: 410px;
        margin: 0 auto;
        background: #ffffff;
        border: 7px solid #e2e8f0;
        border-radius: 36px;
        padding: 12px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
    }
    .phone-top-bar {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 8px 12px;
        margin-bottom: 10px;
    }
    .chat-bubble-customer {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 14px 14px 14px 2px;
        padding: 8px 12px;
        margin-bottom: 6px;
        font-size: 0.82rem;
        color: #1e293b;
    }
    .chat-bubble-seller {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 3.5px solid #3b82f6;
        border-radius: 2px 14px 14px 14px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 0.82rem;
        color: #1e3a8a;
    }
    .chat-bubble-wait {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 3.5px solid #f59e0b;
        border-radius: 2px 14px 14px 14px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 0.80rem;
        color: #92400e;
    }
    .verified-tag {
        background-color: #3b82f6;
        color: #ffffff;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DỮ LIỆU SẢN PHẨM & CHÍNH SÁCH BÁN HÀNG
# ==============================================================================
@st.cache_data
def get_knowledge_base():
    try:
        with open("knowledge_base.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "products": [
                {"id": "P01", "name": "Áo thun Form Rộng Oversize", "price": 199000, "stock": {"M": 15, "L": 20, "XL": 0}, "status": "Còn hàng"},
                {"id": "P02", "name": "Quần Jean Baggy Unisex", "price": 350000, "stock": {"30": 8, "31": 5, "32": 0}, "status": "Còn hàng"},
                {"id": "P03", "name": "Áo Sơ Mi Lụa Hàn Quốc", "price": 250000, "stock": {"M": 0, "L": 0}, "status": "Hết hàng"}
            ],
            "promotions": [
                {"code": "MAGIAM20", "discount": "Giảm 20.000 VNĐ cho đơn từ 200.000 VNĐ", "note": "Áp dụng đơn livestream"}
            ],
            "faqs": {
                "shipping": "Phí ship toàn quốc 30.000 VNĐ. Đơn từ 500.000 VNĐ được Freeship.",
                "return_policy": "Hỗ trợ đổi hàng trong 7 ngày nếu còn nguyên tem mạc."
            }
        }

kb = get_knowledge_base()

# ==============================================================================
# 3. QUẢN LÝ DỮ LIỆU DÙNG CHUNG (SESSION STATE)
# ==============================================================================
if "pinned_deal" not in st.session_state:
    st.session_state.pinned_deal = {
        "id": "P01",
        "name": "Áo thun Form Rộng Oversize",
        "price": 199000,
        "pinned_at": "18:25"
    }

if "stream_comments" not in st.session_state:
    st.session_state.stream_comments = [
        {
            "id": 1,
            "time": "18:25",
            "user": "Hoàng Nam",
            "raw_comment": "Áo thun P01 còn size M không? Ship về 123 Lê Lợi Q1, SĐT 0901234567 cho mình nhé!",
            "masked_comment": "Áo thun P01 còn size M không? Ship về [ĐÃ CHE ĐỊA CHỈ: ***], SĐT 090***4567 cho mình nhé!",
            "has_pii": True,
            "pii_types": ["Số điện thoại", "Địa chỉ"],
            "sentiment": "Tích cực 😊",
            "sentiment_raw": "positive",
            "intent": "Hỏi Tồn Kho & Đặt Hàng",
            "product_id": "P01",
            "risk_level": 2,
            "risk_label": "Cần duyệt (Có SĐT / Địa chỉ)",
            "rag_context": "P01: Giá 199k, size M còn 15 cái. Ship nội thành 30k.",
            "ai_reply": "Dạ Áo thun P01 bên em còn 15 cái size M nha! Giá sale live hôm nay chỉ 199.000đ thôi ạ, shop đã bảo mật SĐT và địa chỉ của bạn để lên đơn sớm nhé!",
            "final_reply": "Dạ Áo thun P01 bên em còn 15 cái size M nha! Giá sale live hôm nay chỉ 199.000đ thôi ạ, shop đã bảo mật SĐT và địa chỉ của bạn để lên đơn sớm nhé!",
            "confidence": 98,
            "status": "Approved"
        },
        {
            "id": 2,
            "time": "18:26",
            "user": "Minh Thư",
            "raw_comment": "Shop bán hàng tắc trách quá, giao chậm 4 ngày làm lỡ việc của tôi! Gọi 0987654321 xử lý ngay!",
            "masked_comment": "Shop bán hàng tắc trách quá, giao chậm 4 ngày làm lỡ việc của tôi! Gọi 098***4321 xử lý ngay!",
            "has_pii": True,
            "pii_types": ["Số điện thoại"],
            "sentiment": "Phàn nàn ⚠️",
            "sentiment_raw": "negative",
            "intent": "Khách khiếu nại giao trễ",
            "product_id": "LOGISTICS",
            "risk_level": 3,
            "risk_label": "Cần xử lý gấp (Khiếu nại)",
            "rag_context": "Chính sách CSKH: Khách khiếu nại cần xin lỗi chân thành và gọi lại hỗ trợ ngay trong 5 phút.",
            "ai_reply": "Dạ shop thành thật xin lỗi vì sự bất tiện này ạ! Chuyên viên chăm sóc khách hàng bên em sẽ gọi lại ngay vào số ***4321 để kiểm tra đơn và giải quyết thỏa đáng cho bạn liền nha!",
            "final_reply": "Dạ shop thành thật xin lỗi vì sự bất tiện này ạ! Chuyên viên chăm sóc khách hàng bên em sẽ gọi lại ngay vào số ***4321 để kiểm tra đơn và giải quyết thỏa đáng cho bạn liền nha!",
            "confidence": 78,
            "status": "Edited & Approved"
        },
        {
            "id": 3,
            "time": "18:27",
            "user": "Khánh Linh",
            "raw_comment": "Áo thun P01 cao 1m62 nặng 51kg mặc size M có bị rộng thùng thình không shop?",
            "masked_comment": "Áo thun P01 cao 1m62 nặng 51kg mặc size M có bị rộng thùng thình không shop?",
            "has_pii": False,
            "pii_types": [],
            "sentiment": "Tích cực 😊",
            "sentiment_raw": "positive",
            "intent": "Tư Vấn Chọn Size",
            "product_id": "P01",
            "risk_level": 1,
            "risk_label": "Tự động gửi",
            "rag_context": "P01: Form rộng oversize, 1m62 51kg mặc size M phủ mông đẹp chuẩn dáng.",
            "ai_reply": "Dạ với chiều cao 1m62 nặng 51kg bạn mặc size M là form rộng phủ mông nhẹ cực xinh và trẻ trung luôn nha!",
            "final_reply": "Dạ với chiều cao 1m62 nặng 51kg bạn mặc size M là form rộng phủ mông nhẹ cực xinh và trẻ trung luôn nha!",
            "confidence": 97,
            "status": "Approved"
        },
        {
            "id": 4,
            "time": "18:28",
            "user": "Quốc Huy",
            "raw_comment": "Áo thun P01 giá bao nhiêu, mua 3 áo có được freeship không?",
            "masked_comment": "Áo thun P01 giá bao nhiêu, mua 3 áo có được freeship không?",
            "has_pii": False,
            "pii_types": [],
            "sentiment": "Tích cực 😊",
            "sentiment_raw": "positive",
            "intent": "Hỏi Giá & Phí Ship",
            "product_id": "P01",
            "risk_level": 1,
            "risk_label": "Tự động gửi",
            "rag_context": "P01: Giá 199k/áo. Đơn từ 500k Freeship toàn quốc.",
            "ai_reply": "Dạ Áo thun P01 giá sale live chỉ 199.000đ/áo thôi ạ! Bạn mua 3 áo là trên 500k nên shop FREESHIP toàn quốc hoàn toàn nha!",
            "final_reply": "Dạ Áo thun P01 giá sale live chỉ 199.000đ/áo thôi ạ! Bạn mua 3 áo là trên 500k nên shop FREESHIP toàn quốc hoàn toàn nha!",
            "confidence": 98,
            "status": "Approved"
        },
        {
            "id": 5,
            "time": "18:29",
            "user": "Bảo Ngọc",
            "raw_comment": "Quần jean baggy P02 size 30 còn hàng không, giá bao nhiêu?",
            "masked_comment": "Quần jean baggy P02 size 30 còn hàng không, giá bao nhiêu?",
            "has_pii": False,
            "pii_types": [],
            "sentiment": "Tích cực 😊",
            "sentiment_raw": "positive",
            "intent": "Hỏi Hàng Tồn & Giá",
            "product_id": "P02",
            "risk_level": 1,
            "risk_label": "Tự động gửi",
            "rag_context": "P02: Giá 350k, size 30 còn 8 chiếc.",
            "ai_reply": "Dạ Quần jean Baggy P02 size 30 hiện còn 8 chiếc ạ! Giá ưu đãi độc quyền trên livestream hôm nay là 350.000đ bạn nha!",
            "final_reply": "Dạ Quần jean Baggy P02 size 30 hiện còn 8 chiếc ạ! Giá ưu đãi độc quyền trên livestream hôm nay là 350.000đ bạn nha!",
            "confidence": 96,
            "status": "Approved"
        },
        {
            "id": 6,
            "time": "18:30",
            "user": "Thanh Trúc",
            "raw_comment": "Shop có voucher nào áp dụng được cho đơn 200k không?",
            "masked_comment": "Shop có voucher nào áp dụng được cho đơn 200k không?",
            "has_pii": False,
            "pii_types": [],
            "sentiment": "Tích cực 😊",
            "sentiment_raw": "positive",
            "intent": "Hỏi Mã Giảm Giá",
            "product_id": "PROMO",
            "risk_level": 1,
            "risk_label": "Tự động gửi",
            "rag_context": "Mã MAGIAM20: Giảm 20.000đ cho đơn từ 200k.",
            "ai_reply": "Dạ shop đang có mã MAGIAM20 giảm ngay 20.000đ cho đơn từ 200k nè! Bạn bấm vào góc giỏ hàng áp mã để được giảm liền nha!",
            "final_reply": "Dạ shop đang có mã MAGIAM20 giảm ngay 20.000đ cho đơn từ 200k nè! Bạn bấm vào góc giỏ hàng áp mã để được giảm liền nha!",
            "confidence": 99,
            "status": "Approved"
        }
    ]

if "active_review_id" not in st.session_state:
    st.session_state.active_review_id = 1


# ==============================================================================
# 4. HÀM TỰ ĐỘNG PHÂN TÍCH VÀ SOẠN CÂU TRẢ LỜI TỰ NHIÊN
# ==============================================================================
def process_customer_comment(comment_text: str, pinned_deal: dict = None):
    """
    Bảo vệ SĐT/địa chỉ + Nhận diện đúng ý khách + Soạn câu trả lời tự nhiên, thân thiện
    """
    masked = comment_text
    pii_types = []

    # 1. Che mờ Số Điện Thoại
    phone_pattern = r"(?:\+?84|0)(?:[3|5|7|8|9])(?:[\s\.\-]?[0-9]){8}"
    phones = re.findall(phone_pattern, masked)
    if phones:
        pii_types.append("Số điện thoại")
        for p in phones:
            digits = re.sub(r"\D", "", p)
            masked = masked.replace(p, f"{digits[:3]}***{digits[-4:]}" if len(digits) >= 9 else "***")

    # 2. Che mờ Địa chỉ giao hàng
    addr_pattern = r"(?:(?:số|địa chỉ)\s+[\d\w\/]+|(?:\d+[\/\d]*\s+[A-Za-zÀ-ỹ\s]+(?:đường|lê lợi|nguyễn trãi|cầu giấy|bình thạnh|quận|huyện|phường|q\d|tp|đà nẵng|hà nội|hcm)[^,\.\n]*))"
    addrs = re.findall(addr_pattern, masked, flags=re.IGNORECASE)
    if addrs:
        pii_types.append("Địa chỉ")
        for a in addrs:
            masked = masked.replace(a, "[ĐÃ CHE ĐỊA CHỈ: ***]")

    has_pii = len(pii_types) > 0
    c_lower = comment_text.lower()

    # 3. Đánh giá Cảm xúc người mua
    neg_tokens = ["vớ vẩn", "chậm", "tệ", "lừa đảo", "bực", "kém", "hỏng", "trễ", "tắc trách", "hoàn tiền", "khiếu nại", "thất vọng"]
    pos_tokens = ["thích", "đẹp", "mua", "chốt", "mê", "nhanh", "yêu", "tốt", "chuẩn", "freeship", "còn hàng", "oke", "ok"]
    
    if any(w in c_lower for w in neg_tokens):
        sentiment = "Phàn nàn ⚠️"
        sentiment_raw = "negative"
    elif any(w in c_lower for w in pos_tokens):
        sentiment = "Tích cực 😊"
        sentiment_raw = "positive"
    else:
        sentiment = "Quan tâm 🤔"
        sentiment_raw = "neutral"

    # 4. Xác định Sản phẩm khách hỏi
    target_prod_id = None
    if any(w in c_lower for w in ["p01", "áo thun", "thun", "oversize"]):
        target_prod_id = "P01"
    elif any(w in c_lower for w in ["p02", "jean", "quần", "baggy", "quần bò"]):
        target_prod_id = "P02"
    elif any(w in c_lower for w in ["p03", "sơ mi", "lụa", "áo sơ mi"]):
        target_prod_id = "P03"

    # Nếu khách chỉ hỏi "còn size M không?", "giá bao nhiêu?", "áo này..." -> ngầm định sản phẩm đang ghim
    prod_inquiry_tokens = ["còn", "hết", "size", "giá", "nhiêu", "tiền", "mẫu này", "áo này", "quần này", "cái này", "sản phẩm này", "đang mặc", "đang ghim", "vải", "chất", "vừa", "kg", "1m", "kho", "chốt", "mua", "đặt"]
    if not target_prod_id and any(w in c_lower for w in prod_inquiry_tokens):
        if pinned_deal and "id" in pinned_deal:
            target_prod_id = pinned_deal["id"]
        elif "pinned_deal" in st.session_state and st.session_state.pinned_deal:
            target_prod_id = st.session_state.pinned_deal.get("id", "P01")
        else:
            target_prod_id = "P01"

    # Nhận diện Size
    detected_size = None
    for s in ["xl", "xxl", "l", "m", "s", "30", "31", "32"]:
        if re.search(r'\b' + s + r'\b', c_lower) or f"size {s}" in c_lower:
            detected_size = s.upper()
            break

    # 5. Soạn câu trả lời giọng điệu bán hàng tự nhiên, niềm nở
    product_id = target_prod_id if target_prod_id else "OTHER"
    confidence = 96

    is_promo = any(w in c_lower for w in ["voucher", "mã", "giảm giá", "magiam20", "khuyến mãi", "ưu đãi", "code", "mgg"])
    is_logistics = any(w in c_lower for w in ["ship", "vận chuyển", "giao hàng", "mấy ngày", "bao lâu", "đổi trả", "freeship", "phí ship", "phí giao"])

    # Khiếu nại
    if sentiment_raw == "negative":
        product_id = target_prod_id if target_prod_id else "LOGISTICS"
        intent = "Khách khiếu nại dịch vụ"
        rag_context = "Chính sách CSKH: Xử lý giao trễ/hàng lỗi với thái độ cầu thị, chuyển chuyên viên CSKH liên hệ xử lý ngay."
        ai_reply = "Dạ shop thành thật xin lỗi vì trải nghiệm chưa hài lòng của bạn ạ! Chuyên viên chăm sóc khách hàng bên em sẽ liên hệ lại qua inbox/SĐT ngay lập tức để kiểm tra và giải quyết quyền lợi nhanh nhất cho bạn nhé!"
        confidence = 78

    # Khuyến mãi / Mã giảm giá
    elif is_promo:
        product_id = "PROMO"
        intent = "Hỏi mã giảm giá"
        rag_context = "Mã MAGIAM20: Giảm 20.000đ cho đơn từ 200.000đ."
        ai_reply = "Dạ trên live hôm nay shop đang có voucher MAGIAM20 giảm ngay 20.000đ cho đơn từ 200k nè! Bạn bấm vào góc giỏ hàng màu vàng áp mã để được giảm trực tiếp nha!"
        confidence = 99

    # Vận chuyển / Đổi trả
    elif is_logistics:
        product_id = "LOGISTICS"
        intent = "Hỏi phí ship & đổi trả"
        rag_context = "Ship toàn quốc 30k. Đơn từ 500k Freeship. Đổi trả trong 7 ngày."
        ai_reply = "Dạ phí ship toàn quốc là 30.000đ bạn nha (giao nhanh 2-3 ngày). Đơn từ 500k shop FREESHIP 100% luôn ạ! Bạn được kiểm tra hàng thoải mái và hỗ trợ đổi size trong 7 ngày nha!"
        confidence = 98

    # Hỏi về Sản phẩm cụ thể
    elif target_prod_id in ["P01", "P02", "P03"]:
        p_obj = next((p for p in kb.get("products", []) if p["id"] == target_prod_id), None)
        p_name = p_obj["name"] if p_obj else target_prod_id
        p_price = p_obj["price"] if p_obj else 199000
        p_stock = p_obj.get("stock", {}) if p_obj else {}
        p_status = p_obj.get("status", "Còn hàng") if p_obj else "Còn hàng"

        # Đã hết hàng hoàn toàn (như P03)
        if p_status == "Hết hàng" or sum(p_stock.values()) == 0:
            intent = f"Hỏi mẫu {target_prod_id} (Đã hết hàng)"
            rag_context = f"{target_prod_id} ({p_name}): Giá {p_price:,}đ. Tình trạng: ĐÃ HẾT HÀNG toàn bộ."
            ai_reply = f"Dạ rất tiếc mẫu {p_name} bên em vừa tạm hết hàng rồi ạ! Bạn tham khảo mẫu Áo thun P01 đang có sẵn đủ size cực xinh trên live nha!"
            confidence = 95

        # Hỏi giá
        elif any(w in c_lower for w in ["giá", "nhiêu", "tiền", "bao nhiêu", "giá sao"]):
            intent = f"Hỏi giá mẫu {target_prod_id}"
            rag_context = f"{target_prod_id} ({p_name}): Giá ưu đãi live {p_price:,}đ."
            ai_reply = f"Dạ mẫu {p_name} giá ưu đãi duy nhất trong phiên live hôm nay chỉ còn {p_price:,}đ thôi ạ! Bạn bấm giỏ hàng góc trái chốt đơn ngay nha!"
            confidence = 99

        # Hỏi đúng một Size cụ thể
        elif detected_size:
            intent = f"Kiểm tra size {detected_size} ({target_prod_id})"
            qty = p_stock.get(detected_size, 0)
            if qty > 0:
                rag_context = f"{target_prod_id} ({p_name}): Size {detected_size} còn {qty} chiếc. Giá {p_price:,}đ."
                ai_reply = f"Dạ mẫu {p_name} hiện CÒN {qty} chiếc size {detected_size} nha! Giá sale live chỉ {p_price:,}đ, bạn nhanh tay bấm chốt đơn kẻo hết size nhé!"
                confidence = 98
            else:
                avail_sizes = [f"size {k} (còn {v} cái)" for k, v in p_stock.items() if v > 0]
                avail_str = ", ".join(avail_sizes) if avail_sizes else "hiện đã tạm hết size"
                rag_context = f"{target_prod_id} ({p_name}): Size {detected_size} HẾT HÀNG. Còn: {avail_str}."
                ai_reply = f"Dạ rất tiếc mẫu {p_name} size {detected_size} bên em vừa hết mất rồi ạ! Kho shop đang còn sẵn {avail_str}, bạn tham khảo đổi size giúp shop nhé!"
                confidence = 96

        # Tư vấn chọn size theo chiều cao, cân nặng
        elif any(w in c_lower for w in ["cao", "nặng", "kg", "vừa", "size gì", "mặc size", "tư vấn size"]):
            intent = f"Tư vấn chọn size {target_prod_id}"
            rag_context = f"{target_prod_id} ({p_name}): Dưới 55kg mặc size M, 55-68kg mặc size L."
            ai_reply = f"Dạ mẫu {p_name} là form rộng thoải mái: Dưới 55kg mặc size M chuẩn xinh, từ 55-68kg mặc size L phủ mông đẹp nha! Bạn có thể nhắn chiều cao và cân nặng để shop chọn size chuẩn nhất cho bạn nè!"
            confidence = 97

        # Hỏi hàng tồn kho nói chung
        elif any(w in c_lower for w in ["còn", "hết", "kho", "sẵn", "mẫu này", "áo này", "quần này", "cái này"]):
            intent = f"Hỏi hàng tồn kho {target_prod_id}"
            avail_sizes = [f"size {k} ({v} cái)" for k, v in p_stock.items() if v > 0]
            avail_str = ", ".join(avail_sizes)
            rag_context = f"{target_prod_id} ({p_name}): Còn hàng: {avail_str}. Giá {p_price:,}đ."
            ai_reply = f"Dạ mẫu {p_name} hiện ĐANG CÒN HÀNG bạn nha! Shop có sẵn: {avail_str}. Giá sale live chỉ {p_price:,}đ, bạn bấm giỏ hàng để chốt sớm nha!"
            confidence = 98

        # Thông tin chung
        else:
            intent = f"Hỏi thông tin {target_prod_id}"
            rag_context = f"{target_prod_id} ({p_name}): Giá {p_price:,}đ."
            ai_reply = f"Dạ mẫu {p_name} chất vải mát mịn, đứng form tôn dáng và đang sale chỉ {p_price:,}đ trên live ạ. Bạn cần shop tư vấn thêm size nào cứ nhắn nhé!"
            confidence = 95

    else:
        # Chào hỏi thân thiện
        intent = "Tương tác chung"
        p_cur = pinned_deal.get("name", "Áo thun P01") if pinned_deal else "Áo thun P01"
        rag_context = f"Đang phát sóng: Ghim mẫu {p_cur}."
        ai_reply = f"Dạ shop chào bạn nha! Bạn đang ưng mẫu {p_cur} đang ghim hay cần tư vấn size, hỏi giá mẫu nào cứ nhắn shop hỗ trợ bạn liền nhé!"
        confidence = 92

    # 6. Mức độ cần người vận hành hỗ trợ
    if sentiment_raw == "negative":
        risk_level = 3
        risk_label = "Cần xử lý gấp (Khiếu nại)"
    elif has_pii:
        risk_level = 2
        risk_label = "Cần duyệt (Có SĐT / Địa chỉ)"
    elif product_id == "P03" or confidence < 90:
        risk_level = 2
        risk_label = "Cần duyệt (Hết hàng / Cần kiểm tra)"
    else:
        risk_level = 1
        risk_label = "Tự động gửi"

    return {
        "raw_comment": comment_text,
        "masked_comment": masked,
        "has_pii": has_pii,
        "pii_types": pii_types,
        "sentiment": sentiment,
        "sentiment_raw": sentiment_raw,
        "intent": intent,
        "product_id": product_id,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "rag_context": rag_context,
        "ai_reply": ai_reply,
        "confidence": confidence
    }

# ==============================================================================
# 5. THANH SIDEBAR ĐIỀU HƯỚNG GỌN GÀNG, DỄ HIỂU
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛍️ Bàn Trợ Lý Live")
    st.caption("Quản lý tương tác và chốt đơn livestream")

    # Tên tính năng thân thiện, tự nhiên
    selected_module = st.radio(
        "Chức năng thao tác:",
        [
            "🛡️ Lọc Tin Nhắn & Bảo Mật",
            "💬 Duyệt & Gửi Câu Trả Lời",
            "📊 Xu Hướng Hỏi Mua & Ghim Deal",
            "📱 Xem Trực Tiếp Trên Live"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("##### 📡 Phiên Live Hiện Tại")
    with st.container(border=True):
        st.markdown("**Shop:** Linh Boutique")
        st.markdown("**Trạng thái:** 🟢 Đang phát sóng")
        st.markdown("**Người xem:** `1,420 mắt xem`")
        if st.session_state.pinned_deal:
            p = st.session_state.pinned_deal
            st.markdown(f"**Đang ghim:** 🔥 `{p['id']}` ({p['price']:,}đ)")
        else:
            st.caption("Chưa có deal ghim.")

    st.markdown("##### 📦 Hàng Trong Kho")
    with st.expander("Danh sách sản phẩm"):
        for prod in kb.get("products", []):
            stock_fmt = ", ".join([f"{k}:{v}" for k, v in prod.get("stock", {}).items()])
            st.write(f"- **{prod['id']}**: {prod['name']} ({prod['price']:,}đ) | Kho: `{stock_fmt}`")
    with st.expander("Chính sách & Khuyến mãi"):
        st.write("- **Voucher:** `MAGIAM20` (Giảm 20k cho đơn từ 200k)")
        st.write("- **Vận chuyển:** 30k toàn quốc (Freeship từ 500k)")
        st.write("- **Đổi hàng:** Hỗ trợ trong 7 ngày")

    st.markdown("---")
    if st.button("🔄 Đặt Lại Dữ Liệu Ban Đầu", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==============================================================================
# 6. HEADER CHÍNH SÁNG & HIỆN ĐẠI
# ==============================================================================
st.markdown("""
<div class="light-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6rem;">🛍️</span>
                <h1>TRỢ LÝ BÁN HÀNG LIVESTREAM</h1>
            </div>
            <p>Tự động trả lời thắc mắc của khách hàng, bảo mật số điện thoại và hỗ trợ ghim sản phẩm bán chạy</p>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 4px;">
            <span class="pill-live">🔴 ĐANG PHÁT TRỰC TIẾP</span>
            <span class="pill-ready">⚡ TRỢ LÝ ĐÃ SẴN SÀNG</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# CHỨC NĂNG 1: LỌC TIN NHẮN & BẢO MẬT
# ==============================================================================
if selected_module == "🛡️ Lọc Tin Nhắn & Bảo Mật":
    st.subheader("🛡️ Lọc Tin Nhắn & Bảo Vệ Thông Tin Khách Hàng")
    st.caption("Kiểm tra nhanh tin nhắn của khách, tự động che mờ số điện thoại / địa chỉ và gợi ý câu trả lời phù hợp:")

    col_input, col_audit = st.columns([1.05, 0.95], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("##### 1. Chọn Hoặc Nhập Tin Nhắn Của Khách")
            
            preset_options = [
                "Áo thun P01 còn size M không? Ship về 123 Lê Lợi Q1, SĐT 0901234567 cho mình nhé!",
                "còn size M không shop ơi?",
                "áo này còn size XL không vậy?",
                "Shop bán hàng tắc trách quá, giao chậm 4 ngày làm lỡ việc của tôi! Gọi 0987654321 xử lý ngay!",
                "Mã giảm giá MAGIAM20 có áp dụng khi mua áo thun P01 không shop?",
                "Quần jean baggy P02 giá bao nhiêu hôm nay, có được thử hàng không?",
                "Áo sơ mi P03 còn hàng size L không shop ơi?"
            ]
            
            chosen_preset = st.selectbox("Chọn câu hỏi thử nghiệm:", preset_options)
            custom_comment = st.text_area("Hoặc nhập câu hỏi bất kỳ từ khách hàng:", placeholder="Ví dụ: còn size M không? / áo này bao nhiêu tiền?...")
            
            active_comment = custom_comment.strip() if custom_comment.strip() else chosen_preset

            btn_inspect = st.button("🔍 Kiểm Tra & Soạn Câu Trả Lời", type="primary", use_container_width=True)

    result = process_customer_comment(active_comment, pinned_deal=st.session_state.pinned_deal)

    with col_audit:
        with st.container(border=True):
            st.markdown("##### 2. Kết Quả Kiểm Tra Tin Nhắn")

            # Bước 1: Che PII
            st.markdown("**1. Bảo vệ thông tin riêng tư (SĐT & Địa chỉ)**")
            if result["has_pii"]:
                st.warning(f"⚠️ Phát hiện thông tin riêng tư: **{', '.join(result['pii_types'])}**")
                st.markdown(f"""
                <div class="mask-preview-box">
                    <span style="color: #64748b;">Nội dung gốc:</span> {result['raw_comment']}<br>
                    <span style="color: #2563eb; font-weight: 600;">Đã che an toàn:</span> <strong style="color: #059669;">{result['masked_comment']}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ Tin nhắn an toàn — Không chứa số điện thoại hoặc địa chỉ cá nhân.")

            st.markdown("---")

            # Bước 2: Ý định & Câu trả lời
            st.markdown("**2. Nội dung câu hỏi & Câu trả lời gợi ý**")
            m_s1, m_s2 = st.columns(2)
            m_s1.metric("Cảm xúc khách", result["sentiment"])
            m_s2.metric("Ý định hỏi", result["intent"])

            st.markdown(f"**Câu trả lời gợi ý (Độ chính xác: {result['confidence']}%):**")
            st.info(f"💬 *\"{result['ai_reply']}\"*")

            st.markdown("---")

            # Bước 3: Mức độ ưu tiên
            st.markdown("**3. Trạng thái xử lý**")
            lvl = result["risk_level"]
            if lvl == 3:
                st.error(f"🔴 **{result['risk_label']}** → Cần gọi điện hoặc nhắn riêng giải quyết cho khách ngay.")
            elif lvl == 2:
                st.warning(f"🟡 **{result['risk_label']}** → Cần shop xem lại và bấm duyệt trước khi phát sóng.")
            else:
                st.success(f"🟢 **{result['risk_label']}** → Đạt chuẩn để trợ lý tự động phản hồi cho khách.")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            if st.button("📥 Chuyển Tin Nhắn Này Sang Danh Sách Chờ Duyệt", use_container_width=True):
                new_entry = {
                    "id": len(st.session_state.stream_comments) + 1,
                    "time": datetime.now().strftime("%H:%M"),
                    "user": f"Khách_{len(st.session_state.stream_comments)+1}",
                    "raw_comment": result["raw_comment"],
                    "masked_comment": result["masked_comment"],
                    "has_pii": result["has_pii"],
                    "pii_types": result["pii_types"],
                    "sentiment": result["sentiment"],
                    "sentiment_raw": result["sentiment_raw"],
                    "intent": result["intent"],
                    "product_id": result["product_id"],
                    "risk_level": result["risk_level"],
                    "risk_label": result["risk_label"],
                    "rag_context": result["rag_context"],
                    "ai_reply": result["ai_reply"],
                    "final_reply": result["ai_reply"],
                    "confidence": result["confidence"],
                    "status": "Pending Review" if lvl >= 2 else "Approved"
                }
                st.session_state.stream_comments.append(new_entry)
                st.session_state.active_review_id = new_entry["id"]
                st.toast(f"Đã lưu tin nhắn #{new_entry['id']} vào hàng chờ!", icon="📋")


# ==============================================================================
# CHỨC NĂNG 2: DUYỆT & GỬI CÂU TRẢ LỜI
# ==============================================================================
elif selected_module == "💬 Duyệt & Gửi Câu Trả Lời":
    st.subheader("💬 Duyệt & Gửi Câu Trả Lời Cho Khách")
    st.caption("Xem trước câu trả lời do trợ lý soạn sẵn, chỉnh sửa theo ý bạn và bấm gửi trực tiếp lên live:")

    col_queue, col_workspace = st.columns([0.8, 1.2], gap="large")

    with col_queue:
        st.markdown("##### 📋 Danh Sách Tin Nhắn Chờ Xử Lý")
        
        all_items = st.session_state.stream_comments
        
        if all_items:
            # Sắp xếp tin nhắn mới nhất lên đầu danh sách chọn
            sorted_items = list(reversed(all_items))
            labels_dict = {
                item["id"]: f"#{item['id']} • [{item['status']}] • {item['masked_comment'][:35]}..."
                for item in sorted_items
            }
            default_idx = 0
            for idx, it in enumerate(sorted_items):
                if it["id"] == st.session_state.active_review_id:
                    default_idx = idx
                    break

            curr_id = st.selectbox(
                "Chọn câu hỏi cần xử lý:",
                options=list(labels_dict.keys()),
                format_func=lambda x: labels_dict[x],
                index=default_idx
            )
            st.session_state.active_review_id = curr_id

            with st.container(border=True):
                st.caption("Tin nhắn gần đây:")
                for it in reversed(all_items[-6:]):
                    dot = "🔴" if "Phàn nàn" in it["sentiment"] else "🟢"
                    st.markdown(f"{dot} **#{it['id']}**: *{it['masked_comment'][:42]}...* (`{it['status']}`)")
        else:
            st.info("Hiện không có tin nhắn nào chờ xử lý.")

    with col_workspace:
        target_item = next((c for c in st.session_state.stream_comments if c["id"] == st.session_state.active_review_id), None)
        
        if target_item:
            with st.container(border=True):
                # Cảnh báo phàn nàn nhẹ nhàng, nổi bật
                if target_item["sentiment_raw"] == "negative" or "Phàn nàn" in target_item["sentiment"]:
                    st.markdown("""
                    <div class="complaint-card">
                        <div class="complaint-title">
                            ⚠️ Khách đang phàn nàn / khiếu nại - Hãy ưu tiên giải quyết ngay!
                        </div>
                        <div class="complaint-body">
                            Tin nhắn này có nội dung bức xúc. Shop vui lòng đọc kỹ, điều chỉnh lại câu từ khéo léo để hỗ trợ khách tốt nhất trước khi gửi nhé!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("**Câu hỏi của khách (Đã che thông tin riêng tư):**")
                st.info(f"💬 *\"{target_item['masked_comment']}\"*")

                with st.expander("📚 Thông tin kho & chính sách đối chiếu", expanded=True):
                    st.write(target_item.get("rag_context", "Dữ liệu tra cứu sản phẩm."))

                c_m1, c_m2, c_m3 = st.columns(3)
                c_m1.metric("Ý định của khách", target_item["intent"])
                c_m2.metric("Thái độ", target_item["sentiment"])
                c_m3.metric("Độ tin cậy gợi ý", f"{target_item['confidence']}%")

                st.markdown("---")

                st.markdown("**Câu trả lời gợi ý (Shop có thể sửa lại theo ý mình trước khi bấm gửi):**")
                operator_text = st.text_area(
                    label="Nội dung gửi cho khách",
                    value=target_item["final_reply"] if target_item.get("final_reply") else target_item["ai_reply"],
                    height=100,
                    label_visibility="collapsed"
                )

                st.caption("Lựa chọn thao tác:")
                act1, act2, act3 = st.columns(3)

                with act1:
                    if st.button("✅ Duyệt & Gửi Ngay", type="primary", use_container_width=True):
                        target_item["final_reply"] = operator_text
                        target_item["status"] = "Approved"
                        st.session_state["live_notification"] = {
                            "type": "success",
                            "title": f"Shop đã duyệt & gửi câu trả lời #{target_item['id']} lên live!",
                            "msg": operator_text,
                            "user": target_item.get("user", "Khách hàng")
                        }
                        st.toast(f"Đã duyệt và gửi câu trả lời #{target_item['id']}!", icon="🚀")
                        st.rerun()

                with act2:
                    if st.button("✏️ Đã Sửa & Gửi Đi", use_container_width=True):
                        target_item["final_reply"] = operator_text
                        target_item["status"] = "Edited & Approved"
                        st.session_state["live_notification"] = {
                            "type": "success",
                            "title": f"Shop đã chỉnh sửa & gửi câu trả lời #{target_item['id']} lên live!",
                            "msg": operator_text,
                            "user": target_item.get("user", "Khách hàng")
                        }
                        st.toast(f"Đã lưu nội dung sửa và gửi câu trả lời #{target_item['id']}!", icon="✍️")
                        st.rerun()

                with act3:
                    if st.button("❌ Bỏ Qua Tin Này", use_container_width=True):
                        target_item["status"] = "Rejected"
                        st.session_state["live_notification"] = {
                            "type": "warning",
                            "title": f"Shop đã bỏ qua tin nhắn #{target_item['id']}",
                            "msg": "Tin nhắn này sẽ không phát sóng trên livestream.",
                            "user": target_item.get("user", "Khách hàng")
                        }
                        st.toast(f"Đã bỏ qua tin nhắn #{target_item['id']}!", icon="🗑️")
                        st.rerun()
        else:
            st.info("Vui lòng chọn một tin nhắn từ danh sách bên trái để thao tác.")


# ==============================================================================
# CHỨC NĂNG 3: XU HƯỚNG HỎI MUA & GHIM DEAL
# ==============================================================================
elif selected_module == "📊 Xu Hướng Hỏi Mua & Ghim Deal":
    st.subheader("📊 Xu Hướng Hỏi Mua & Gợi Ý Ghim Deal Bán Chạy")
    st.caption("Xem khách đang quan tâm sản phẩm nào nhiều nhất trong buổi live để kịp thời ghim deal ưu đãi lên đầu màn hình:")

    comments_pool = st.session_state.stream_comments
    total_inquiries = len(comments_pool)

    # Chỉ số bán hàng dễ hiểu
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Tổng lượt khách hỏi", f"{total_inquiries} câu hỏi")
    approved_total = sum(1 for c in comments_pool if "Approved" in c["status"])
    kpi2.metric("Đã trả lời cho khách", f"{approved_total} câu trả lời")
    
    pos_total = sum(1 for c in comments_pool if "Tích cực" in c["sentiment"])
    neg_total = sum(1 for c in comments_pool if "Phàn nàn" in c["sentiment"])
    neu_total = total_inquiries - pos_total - neg_total
    
    kpi3.metric("Tỷ lệ phản hồi tích cực", f"{round((pos_total/max(total_inquiries, 1))*100)}%")
    kpi4.metric("Số lượt cần hỗ trợ gấp", f"{neg_total} khách", delta=f"{neg_total} phàn nàn", delta_color="inverse")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    col_donut, col_groups = st.columns([0.85, 1.15], gap="large")

    with col_donut:
        with st.container(border=True):
            st.markdown("##### 🎯 Tỷ Lệ Cảm Xúc Của Khách Hàng")
            st.caption("Thống kê mức độ hài lòng và quan tâm của khách xem live:")

            total_calc = max(total_inquiries, 1)
            pos_pct = round((pos_total / total_calc) * 100, 1)
            neu_pct = round((neu_total / total_calc) * 100, 1)
            neg_pct = max(0.0, round(100.0 - pos_pct - neu_pct, 1))

            offset1 = 25.0
            offset2 = (offset1 - pos_pct) % 100.0
            offset3 = (offset2 - neu_pct) % 100.0

            # Biểu đồ Donut thuần SVG siêu nhẹ, không phụ thuộc thư viện ngoài, không bị lỗi numpy
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 12px 0;">
                <svg viewBox="0 0 42 42" style="width: 190px; height: 190px; max-width: 100%; border-radius: 50%;">
                    <circle cx="21" cy="21" r="15.91549430918954" fill="#ffffff" stroke="#f1f5f9" stroke-width="5.5"></circle>
                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#10b981" stroke-width="5.5"
                            stroke-dasharray="{pos_pct} {100 - pos_pct}" stroke-dashoffset="{offset1}"></circle>
                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#3b82f6" stroke-width="5.5"
                            stroke-dasharray="{neu_pct} {100 - neu_pct}" stroke-dashoffset="{offset2}"></circle>
                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ef4444" stroke-width="5.5"
                            stroke-dasharray="{neg_pct} {100 - neg_pct}" stroke-dashoffset="{offset3}"></circle>
                    <text x="50%" y="46%" font-size="5" font-weight="800" text-anchor="middle" fill="#0f172a">{pos_pct:.0f}%</text>
                    <text x="50%" y="58%" font-size="2.6" font-weight="600" text-anchor="middle" fill="#64748b">Hài lòng</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin-top: 8px; font-size: 0.85rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🟢 <strong>Tích cực:</strong></span>
                    <span style="font-weight: 700; color: #059669;">{pos_total} lượt ({pos_pct:.0f}%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🔵 <strong>Quan tâm hỏi thêm:</strong></span>
                    <span style="font-weight: 700; color: #2563eb;">{neu_total} lượt ({neu_pct:.0f}%)</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>🔴 <strong>Cần hỗ trợ gấp:</strong></span>
                    <span style="font-weight: 700; color: #dc2626;">{neg_total} lượt ({neg_pct:.0f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_groups:
        with st.container(border=True):
            st.markdown("##### 🧩 Các Nhóm Câu Hỏi Khách Quan Tâm Nhất")
            st.caption("Tự động tổng hợp các thắc mắc cùng chủ đề giúp shop nắm bắt nhu cầu:")

            cluster_dict = {}
            for c in comments_pool:
                k = f"{c['product_id']} | {c['intent']}"
                if k not in cluster_dict:
                    cluster_dict[k] = {
                        "product": c["product_id"],
                        "intent": c["intent"],
                        "count": 0,
                        "sample": c["masked_comment"]
                    }
                cluster_dict[k]["count"] += 1

            for _, val in sorted(cluster_dict.items(), key=lambda x: x[1]["count"], reverse=True):
                share = round((val["count"] / max(total_inquiries, 1)) * 100)
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #1e293b; font-size: 0.9rem;">{val['intent']}</strong>
                        <span style="background: #eef2ff; color: #4338ca; padding: 2px 8px; border-radius: 6px; font-size: 0.76rem; font-weight: 700;">
                            {val['count']} lượt hỏi ({share}%)
                        </span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                        Ví dụ câu hỏi: <em>"{val['sample'][:65]}..."</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Thẻ gợi ý Ghim Deal tự nhiên
    counts = Counter([c["product_id"] for c in comments_pool if c["product_id"] in ["P01", "P02", "P03"]])
    top_p_id, top_p_cnt = counts.most_common(1)[0] if counts else ("P01", 3)

    p_info = next((p for p in kb.get("products", []) if p["id"] == top_p_id), None)
    p_name = p_info["name"] if p_info else "Áo thun Form Rộng Oversize"
    p_price = p_info["price"] if p_info else 199000

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="deal-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <span class="deal-badge">🔥 GỢI Ý BÁN CHẠY: NÊN GHIM DEAL NGAY</span>
            <span style="color: #9a3412; font-weight: 700; font-size: 0.82rem;">
                Có {top_p_cnt} khách đang hỏi về mẫu này
            </span>
        </div>
        <div style="font-size: 1.25rem; font-weight: 800; color: #9a3412; margin: 8px 0 4px 0;">
            SẢN PHẨM ĐƯỢC QUAN TÂM NHIỀU NHẤT: {top_p_id} — {p_name.upper()}
        </div>
        <div style="color: #7c2d12; font-size: 0.88rem; line-height: 1.45;">
            Nhiều khách đang hỏi size và giá mẫu <strong>{p_name}</strong>. 
            Shop nên <strong>ghim sản phẩm này lên đầu màn hình</strong> ngay để chốt đơn nhanh hơn nhé!
        </div>
    </div>
    """, unsafe_allow_html=True)

    btn_pin_c1, btn_pin_c2 = st.columns([1, 2])
    with btn_pin_c1:
        if st.button("📌 BẤM ĐỂ GHIM DEAL NÀY LÊN LIVE", type="primary", use_container_width=True):
            st.session_state.pinned_deal = {
                "id": top_p_id,
                "name": p_name,
                "price": p_price,
                "pinned_at": datetime.now().strftime("%H:%M")
            }
            st.toast(f"Đã ghim deal {top_p_id} lên màn hình người xem!", icon="📌")
            st.rerun()

    with btn_pin_c2:
        if st.session_state.pinned_deal:
            cur = st.session_state.pinned_deal
            st.success(f"🟢 **Đang ghim trên live:** `{cur['id']} - {cur['name']}` ({cur['price']:,}đ) từ lúc {cur.get('pinned_at', 'vừa xong')}.")


# ==============================================================================
# CHỨC NĂNG 4: XEM TRỰC TIẾP TRÊN LIVE
# ==============================================================================
elif selected_module == "📱 Xem Trực Tiếp Trên Live":
    st.subheader("📱 Xem Trực Tiếp Trên Màn Hình Livestream")
    st.caption("Xem thực tế bình luận của khách và câu trả lời của shop hiển thị như trên điện thoại người xem:")

    col_mockup, col_live_act = st.columns([1.05, 0.95], gap="large")

    with col_mockup:
        # 1. Chuẩn bị danh sách tin nhắn chat trong livestream
        chat_bubbles_html = []
        feed = [c for c in st.session_state.stream_comments if "Approved" in c["status"] or c["status"] == "Pending Review"]
        if feed:
            for idx, f in enumerate(reversed(feed[-15:])):
                is_approved = "Approved" in f["status"]
                is_manual = "Edited" in f["status"]
                pill_label = "Shop đã duyệt" if is_manual else "Trợ lý Shop"
                is_newest = (idx == 0)
                new_tag = '<span style="background: #10b981; color: white; font-size: 0.62rem; font-weight: 800; padding: 1px 5px; border-radius: 4px; margin-left: 6px;">VỪA GỬI 🔥</span>' if is_newest else ""

                b_cust = f"""
                <div class="chat-bubble-customer" style="background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 14px 14px 14px 2px; padding: 8px 12px; margin-bottom: 6px; font-size: 0.82rem; color: #1e293b; {'border: 1.5px solid #3b82f6;' if is_newest else ''}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                        <div>
                            <strong style="color: #2563eb;">{f.get('user', 'Khách hàng')}</strong>
                            {new_tag}
                        </div>
                        <span style="font-size: 0.70rem; color: #64748b;">{f.get('time', 'Vừa xong')}</span>
                    </div>
                    <div>{f['masked_comment']}</div>
                </div>
                """
                chat_bubbles_html.append(b_cust)

                if is_approved:
                    final_text = f.get('final_reply') or f.get('ai_reply', '')
                    b_sel = f"""
                    <div class="chat-bubble-seller" style="background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #10b981; border-radius: 2px 14px 14px 14px; padding: 8px 12px; margin-bottom: 10px; font-size: 0.82rem; color: #1e3a8a;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                            <span style="color: #1d4ed8; font-weight: 700;">💬 Trợ lý Livestream</span>
                            <span class="verified-tag" style="background: #3b82f6; color: white; font-size: 0.65rem; font-weight: 700; padding: 1px 6px; border-radius: 4px;">{pill_label}</span>
                        </div>
                        <div>{final_text}</div>
                    </div>
                    """
                    chat_bubbles_html.append(b_sel)
                else:
                    b_wait = """
                    <div class="chat-bubble-wait" style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #f59e0b; border-radius: 2px 14px 14px 14px; padding: 8px 12px; margin-bottom: 10px; font-size: 0.80rem; color: #92400e;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                            <span style="font-weight: 700; color: #b45309;">💬 Trợ lý Livestream</span>
                            <span style="background: #fde68a; color: #92400e; font-size: 0.65rem; padding: 1px 6px; border-radius: 4px; font-weight: 600;">Shop đang duyệt</span>
                        </div>
                        <div><em>⏳ Tin nhắn đang được shop kiểm tra trước khi gửi lên live...</em></div>
                    </div>
                    """
                    chat_bubbles_html.append(b_wait)
        else:
            chat_bubbles_html.append("<div style='text-align: center; color: #94a3b8; padding: 35px 0;'>Chưa có bình luận nào trên live.</div>")

        joined_chats = "".join(chat_bubbles_html)

        # 2. Deal đang ghim (nếu có)
        deal_banner_html = ""
        if st.session_state.pinned_deal:
            d = st.session_state.pinned_deal
            deal_banner_html = f"""
            <div style="background: linear-gradient(90deg, #ea580c 0%, #f97316 100%); border-radius: 8px; padding: 8px 12px; color: white; margin-bottom: 10px; font-size: 0.78rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>🔥 ĐANG GHIM: {d['id']}</strong><br>
                    <span>{d['name']} — <strong>{d['price']:,}đ</strong></span>
                </div>
                <span style="background: #fef08a; color: #854d0e; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 0.7rem;">
                    MUA NGAY
                </span>
            </div>
            """

        # 3. Thông báo đẩy trên Livestream (Real-time Push Notification)
        live_push_notif_html = ""
        if st.session_state.get("live_notification"):
            notif = st.session_state["live_notification"]
            is_ok = notif.get("type") == "success"
            b_bg = "#ecfdf5" if is_ok else "#fffbeb"
            b_border = "#10b981" if is_ok else "#f59e0b"
            b_color = "#065f46" if is_ok else "#92400e"
            icon_n = "🔔" if is_ok else "⏳"
            live_push_notif_html = f"""
            <div style="background: {b_bg}; border: 1.5px solid {b_border}; border-radius: 8px; padding: 7px 10px; margin-bottom: 9px; font-size: 0.76rem; color: {b_color}; display: flex; align-items: center; justify-content: space-between;">
                <div><strong>{icon_n} Thông báo đẩy:</strong> {notif.get('title', 'Vừa cập nhật')}</div>
                <span style="background: {b_border}; color: white; font-size: 0.62rem; font-weight: 800; padding: 1px 5px; border-radius: 4px;">VỪA XONG</span>
            </div>
            """

        # 4. Ảnh minh họa phòng Live Studio dạng SVG sắc nét, không bị phụ thuộc mạng
        studio_svg_code = """<svg viewBox="0 0 400 215" width="100%" height="215" xmlns="http://www.w3.org/2000/svg" style="display: block;">
  <defs>
    <linearGradient id="liveBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1b4b"/>
      <stop offset="45%" stop-color="#312e81"/>
      <stop offset="100%" stop-color="#4f46e5"/>
    </linearGradient>
    <linearGradient id="liveGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f43f5e"/>
      <stop offset="100%" stop-color="#fb923c"/>
    </linearGradient>
    <linearGradient id="p01Shirt" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#eab308"/>
    </linearGradient>
  </defs>

  <!-- Phòng Live Studio -->
  <rect width="400" height="215" fill="url(#liveBg)"/>
  
  <!-- Ánh sáng sân khấu Studio -->
  <circle cx="80" cy="45" r="70" fill="#818cf8" opacity="0.2"/>
  <circle cx="330" cy="55" r="85" fill="#f472b6" opacity="0.25"/>
  <circle cx="210" cy="110" r="100" fill="#ffffff" opacity="0.06"/>

  <!-- Kệ quần áo phía sau Studio -->
  <line x1="35" y1="75" x2="135" y2="75" stroke="#94a3b8" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="45" y1="75" x2="45" y2="185" stroke="#64748b" stroke-width="2.5"/>
  <line x1="125" y1="75" x2="125" y2="185" stroke="#64748b" stroke-width="2.5"/>
  
  <!-- Móc quần áo treo mẫu -->
  <path d="M55 77 L65 98 L45 98 Z" fill="#38bdf8" opacity="0.8"/>
  <rect x="48" y="98" width="14" height="48" rx="2" fill="#38bdf8" opacity="0.8"/>
  <path d="M80 77 L90 98 L70 98 Z" fill="#f472b6" opacity="0.8"/>
  <rect x="73" y="98" width="14" height="54" rx="2" fill="#f472b6" opacity="0.8"/>
  <path d="M105 77 L115 98 L95 98 Z" fill="#a78bfa" opacity="0.8"/>
  <rect x="98" y="98" width="14" height="44" rx="2" fill="#a78bfa" opacity="0.8"/>

  <!-- Vòng đèn Ring Light livestream -->
  <circle cx="225" cy="100" r="56" fill="none" stroke="#ffffff" stroke-width="4.5" opacity="0.4" stroke-dasharray="8 5"/>
  
  <!-- Thân mẫu / Host livestream -->
  <ellipse cx="225" cy="190" rx="48" ry="38" fill="#ffffff" opacity="0.95"/>
  
  <!-- Sản phẩm P01 đang được Host cầm giơ lên giới thiệu -->
  <path d="M198 135 L215 124 L235 124 L252 135 L246 152 L238 148 L238 190 L212 190 L212 148 L204 152 Z" fill="url(#p01Shirt)"/>
  <text x="225" y="162" font-family="Arial, sans-serif" font-size="10" font-weight="900" fill="#78350f" text-anchor="middle">P01</text>
  <text x="225" y="174" font-family="Arial, sans-serif" font-size="8" font-weight="700" fill="#92400e" text-anchor="middle">199.000đ</text>
  
  <!-- Cổ và Khuôn mặt Host Livestream -->
  <rect x="220" y="95" width="10" height="16" fill="#fed7aa" rx="2"/>
  <ellipse cx="225" cy="85" rx="19" ry="23" fill="#fed7aa"/>
  <!-- Mái tóc sành điệu -->
  <path d="M204 84 Q225 54 246 84 Q252 112 244 122 Q240 100 240 90 Q225 78 210 90 Q210 100 206 122 Q198 112 204 84 Z" fill="#3b1d11"/>
  <!-- Đôi mắt cười thân thiện -->
  <circle cx="218" cy="85" r="2.2" fill="#3b1d11"/>
  <circle cx="232" cy="85" r="2.2" fill="#3b1d11"/>
  <!-- Nụ cười duyên -->
  <path d="M220 93 Q225 98 230 93" stroke="#ea580c" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <!-- Má hồng xinh xắn -->
  <circle cx="215" cy="90" r="3.5" fill="#f43f5e" opacity="0.45"/>
  <circle cx="235" cy="90" r="3.5" fill="#f43f5e" opacity="0.45"/>
  <!-- Tay giữ áo -->
  <ellipse cx="196" cy="144" rx="6" ry="8" fill="#fed7aa" transform="rotate(-20 196 144)"/>
  <ellipse cx="254" cy="144" rx="6" ry="8" fill="#fed7aa" transform="rotate(20 254 144)"/>

  <!-- Hiệu ứng Tim & Lửa bay lên liên tục -->
  <g opacity="0.95">
    <text x="345" y="125" font-size="20">💖</text>
    <text x="365" y="90" font-size="24">❤️</text>
    <text x="338" y="60" font-size="18">🔥</text>
    <text x="360" y="155" font-size="16">👏</text>
    <text x="330" y="180" font-size="18">🛍️</text>
  </g>

  <!-- Lớp phủ giao diện Livestream -->
  <!-- Nút ĐANG LIVE -->
  <rect x="12" y="12" width="66" height="23" rx="11.5" fill="#ef4444"/>
  <circle cx="22" cy="23.5" r="4" fill="#ffffff"/>
  <text x="33" y="27.5" font-family="Arial, sans-serif" font-size="10.5" font-weight="900" fill="#ffffff">LIVE</text>

  <!-- Mắt xem -->
  <rect x="84" y="12" width="90" height="23" rx="11.5" fill="rgba(0,0,0,0.5)"/>
  <text x="129" y="27" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#ffffff" text-anchor="middle">👁️ 1.4k xem</text>

  <!-- Tên Shop & Thông tin phiên live -->
  <rect x="12" y="178" width="138" height="26" rx="7" fill="rgba(0,0,0,0.65)"/>
  <text x="18" y="195" font-family="Arial, sans-serif" font-size="10.5" font-weight="800" fill="#fef08a">🛍️ Linh Boutique</text>

  <!-- Huy hiệu Giảm giá độc quyền -->
  <rect x="255" y="178" width="133" height="26" rx="7" fill="url(#liveGlow)"/>
  <text x="321" y="195" font-family="Arial, sans-serif" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">⚡ VOUCHER: -20K</text>
</svg>"""

        # 5. Lắp ráp toàn bộ giao diện điện thoại smartphone hoàn chỉnh
        phone_markup = f"""<div class="phone-mockup" style="max-width: 410px; margin: 0 auto; background: #ffffff; border: 7px solid #e2e8f0; border-radius: 36px; padding: 12px; box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);">
    <!-- Thanh đỉnh điện thoại -->
    <div class="phone-top-bar" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px 12px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 9999px; font-weight: 800; font-size: 0.7rem;">🔴 LIVE</span>
                <strong style="font-size: 0.84rem; color: #1e293b;">Linh Boutique</strong>
            </div>
            <span style="font-size: 0.74rem; color: #64748b;">👁️ 1,420 người xem</span>
        </div>
    </div>

    <!-- Khung video livestream minh họa -->
    <div style="border-radius: 14px; overflow: hidden; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 1px solid #cbd5e1;">
        {studio_svg_code}
    </div>

    <!-- Banner Deal ghim -->
    {deal_banner_html}

    <!-- Thông báo đẩy trên live -->
    {live_push_notif_html}

    <!-- Khung bình luận trực tiếp (Tin mới nhất ở trên đầu) -->
    <div style="height: 380px; overflow-y: auto; padding-right: 4px;">
        {joined_chats}
    </div>
</div>"""

        # Sử dụng st.html trực tiếp để bảo đảm hiển thị HTML chuẩn 100%, không bị chuyển thành mã code
        st.html(phone_markup)

    with col_live_act:
        with st.container(border=True):
            st.markdown("##### 💬 Gõ Thử Bình Luận Khách Xem Live")
            st.caption("Thử nhập câu hỏi bất kỳ như một người xem thật để xem trợ lý trả lời:")

            # Hiển thị thông báo đẩy ở khung điều khiển
            if st.session_state.get("live_notification"):
                notif = st.session_state["live_notification"]
                if notif.get("type") == "success":
                    st.success(f"🔔 **Thông Báo Đẩy:** Trợ lý vừa phản hồi cho **{notif.get('user', 'khách')}**:\n\n*\"{notif.get('msg', '')}\"*")
                else:
                    st.warning(f"🔔 **Thông Báo Đẩy:** Câu hỏi của **{notif.get('user', 'khách')}** chứa SĐT / Khiếu nại — Đã chuyển sang mục **'Duyệt & Gửi Câu Trả Lời'** để duyệt an toàn!")

            st.markdown("**Bấm nhanh câu hỏi mẫu:**")
            quick_cols = st.columns(2)
            with quick_cols[0]:
                if st.button("👕 Còn size M không shop?", use_container_width=True):
                    st.session_state["quick_chat_input"] = "còn size M không shop?"
                if st.button("❌ Áo này còn size XL không?", use_container_width=True):
                    st.session_state["quick_chat_input"] = "áo này còn size XL không?"
            with quick_cols[1]:
                if st.button("💰 Mẫu này giá bao nhiêu?", use_container_width=True):
                    st.session_state["quick_chat_input"] = "mẫu này giá bao nhiêu vậy shop?"
                if st.button("👖 Quần jean P02 còn size 30 không?", use_container_width=True):
                    st.session_state["quick_chat_input"] = "quần jean P02 còn size 30 không?"

            default_text = st.session_state.get("quick_chat_input", "")

            sim_name = st.text_input("Tên người xem:", value="Khách_Xem_Live")
            sim_comment = st.text_area(
                "Nội dung bình luận trên live:", 
                value=default_text,
                placeholder="Ví dụ: còn size M không? / áo này bao nhiêu tiền? / ship về Đà Nẵng mấy ngày?..."
            )

            if st.button("📤 Gửi Lên Livestream", type="primary", use_container_width=True):
                if sim_comment.strip():
                    checked = process_customer_comment(sim_comment.strip(), pinned_deal=st.session_state.pinned_deal)
                    new_chat = {
                        "id": len(st.session_state.stream_comments) + 1,
                        "time": datetime.now().strftime("%H:%M"),
                        "user": sim_name,
                        "raw_comment": checked["raw_comment"],
                        "masked_comment": checked["masked_comment"],
                        "has_pii": checked["has_pii"],
                        "pii_types": checked["pii_types"],
                        "sentiment": checked["sentiment"],
                        "sentiment_raw": checked["sentiment_raw"],
                        "intent": checked["intent"],
                        "product_id": checked["product_id"],
                        "risk_level": checked["risk_level"],
                        "risk_label": checked["risk_label"],
                        "rag_context": checked["rag_context"],
                        "ai_reply": checked["ai_reply"],
                        "final_reply": checked["ai_reply"],
                        "confidence": checked["confidence"],
                        "status": "Pending Review" if checked["risk_level"] >= 2 else "Approved"
                    }
                    st.session_state.stream_comments.append(new_chat)
                    st.session_state.active_review_id = new_chat["id"]
                    
                    if "quick_chat_input" in st.session_state:
                        st.session_state["quick_chat_input"] = ""

                    if new_chat["status"] == "Approved":
                        st.session_state["live_notification"] = {
                            "type": "success",
                            "title": "Trợ lý đã tự động phản hồi câu hỏi!",
                            "msg": checked['ai_reply'],
                            "user": sim_name
                        }
                        st.toast(f"Trợ lý đã trả lời: \"{checked['ai_reply'][:38]}...\"", icon="💬")
                    else:
                        st.session_state["live_notification"] = {
                            "type": "warning",
                            "title": "Tin nhắn đã chuyển sang mục 'Duyệt & Gửi Câu Trả Lời'!",
                            "msg": "Tin nhắn có chứa số điện thoại hoặc khiếu nại, cần duyệt trước khi hiển thị.",
                            "user": sim_name
                        }
                        st.toast(f"Tin nhắn đã được chuyển sang mục 'Duyệt Câu Trả Lời'!", icon="📋")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung câu hỏi trước khi bấm gửi!")
