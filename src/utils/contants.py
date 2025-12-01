MODEL_PATH = 'model'
SENTIMENT_LABEL_PARAMETER = [-1,0,1]
LOCATION_TAG = {

# Activity Domain
"Activity": {
    "Cultural/Historic": [
        "di sản",
        "bảo tàng",
        "di tích",
        "tôn giáo",
        "chùa",
        "nhà thờ",
        "di sản ít người biết",  
        "di tích nổi tiếng"
    ],
    "Nature/Outdoor": [
        "công viên quốc gia",
        "bãi biển",
        "núi non",
        "khu bảo tồn",
        "cảnh quan thiên nhiên hoang sơ",
        "có view panorama",
        "thích trekking / leo núi"
    ],
    "Entertainment/Leisure": [
        "rạp chiếu phim",
        "quán bar",
        "club",
        "công viên giải trí",
        "nhạc sống / show diễn",
        "trò chơi cảm giác mạnh"
    ],
    "Gastronomy/Food": [
        "nhà hàng",
        "quán cà phê",
        "ẩm thực đường phố",
        "mua sắm ẩm thực",
        "ẩm thực đặc sản",
        "food tour / trải nghiệm ẩm thực"
    ]
},

# Budget / Constraint Domain
"Budget": {
    "Budget Level": [
        "giá rẻ",
        "giá hợp lý",
        "giá mắc",
        "luxury / sang trọng",
        "sang trọng"
    ]
},

# Social Context Domain
"Social Context": {
    "Group Type": [
        "cá nhân",
        "cặp đôi",
        "gia đình",
        "bạn bè",
        "nhóm đông / team building"
    ],
    "Crowd Level": [
        "yên tĩnh",
        "riêng tư",
        "đông đúc vừa phải",
        "rất náo nhiệt"
    ]
},

# Amenities / Support Services
"Amenities": {
    "Facilities": [
        "lưu trú",
        "bãi đỗ xe",
        "nhà vệ sinh công cộng",
        "wifi / internet",
        "cơ sở vật chất tốt",
        "an toàn",
        "có hướng dẫn viên",
        "tour tự do / linh hoạt"
    ],
    "Accessibility": [
        "phù hợp trẻ em",
        "phù hợp người cao tuổi",
        "thân thiện người khuyết tật",
        "gần trung tâm / dễ đi lại"
    ]
},

# Accessibility / Travel Convenience
"Accessibility": [
    "dễ đến",
    "xa trung tâm",
    "đường tốt / thuận tiện di chuyển",
    "phù hợp đi bộ nhiều",
    "thuận tiện đi xe máy / xe bus / taxi"
],

# Tourism Type / Travel Motive
"Tourism Type": [
    "du lịch sinh thái",
    "du lịch nghỉ dưỡng",
    "du lịch tâm linh",
    "du lịch cộng đồng",
    "du lịch mạo hiểm / khám phá",
    "du lịch wellness / spa",
    "du lịch lễ hội / sự kiện",
    "du lịch học hỏi / trải nghiệm văn hóa",
    "du lịch ẩm thực",
    "du lịch chụp ảnh / nhiếp ảnh"
],

# Time / Season
"Time": [
    "mùa cao điểm",
    "mùa thấp điểm",
    "buổi sáng",
    "buổi chiều",
    "buổi tối",
    "theo mùa / thời tiết",
    "theo lịch lễ hội / sự kiện"
],

# Experience Preference / User Preference
"Experience Preference": [
    "thích thiên nhiên",
    "thích phiêu lưu / mạo hiểm",
    "thích nghỉ dưỡng / thư giãn",
    "phù hợp gia đình",
    "phù hợp nhóm bạn",
    "phù hợp cặp đôi / hẹn hò",
    "khám phá văn hóa / kiến thức",
    "thích chụp ảnh",
    "thích trải nghiệm địa phương / authentic",
    "thích nightlife / sôi động",
    "thích yên tĩnh / riêng tư"
]
}

def get_tags_list():
    tags = []
    for domain, sub in LOCATION_TAG.items():
        if isinstance(sub, dict):
            for key, lst in sub.items():
                if isinstance(lst, dict):
                    for subkey, sublst in lst.items():
                        tags.extend(sublst)
                else:
                    tags.extend(lst)
        else:
            tags.extend(sub)
    return tags
