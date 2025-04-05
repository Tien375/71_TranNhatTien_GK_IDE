def clean_gold_data(raw_data):
    cleaned_data = []
    for item in raw_data:
        try:
            buy = float(item['buy'].replace('.', ''))
            sell = float(item['sell'].replace('.', ''))
            cleaned_data.append({
                'location': item.get('location'),
                'brand': item['brand'],
                'buy': buy,
                'sell': sell
            })
        except Exception as e:
            print(f"Lỗi xử lý dòng: {item} -> {e}")
    return cleaned_data
