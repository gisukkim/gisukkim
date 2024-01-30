import pyupbit
import time

# 업비트 API Key 및 Secret 설정
access_key = "yvwVKtlGJHoCixsvLDKCxVvkOXMnShFLCjXihxfs"
secret_key = "cXqC7dt55F2hmKos59vxgxjmE2Xl86LMO3GVeNh8"
upbit = pyupbit.Upbit(access_key, secret_key)

# 매수/매도 비율 설정 (1.0은 전체 잔고를 의미)
buy_ratio = 0.15  # 100% 매수
sell_ratio = 1.0  # 100% 매도

# 매수/매도 조건 설정
buy_condition = lambda current_price, ma: current_price > ma  # 5분봉 현재가가 이동평균을 넘으면 매수
sell_condition = lambda current_price, ma: current_price < ma  # 5분봉 현재가가 이동평균 미만이면 매도

# 이동평균 계산 함수
def calculate_ma(ticker, interval, window):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=window)
    ma = df['close'].rolling(window=window).mean().iloc[-1]
    return ma

# 메인 루프
def main():
    ticker = "KRW-BTC"  # 비트코인을 예시로 사용
    interval = "minute5"  # 5분봉을 사용
    window = 8  # 이동평균 창 크기

    while True:
        try:
            # 현재가 및 이동평균 계산
            current_price = pyupbit.get_current_price(ticker)
            ma = calculate_ma(ticker, interval, window)

            # 사용 가능한 잔고 조회
            balance = upbit.get_balance(ticker)
                        # 사용 가능한 KRW 잔고 조회
            krw_balance = upbit.get_balance("KRW")

            # 매수/매도 결정 및 주문 실행
            if buy_condition(current_price, ma):
                upbit.buy_market_order(ticker, krw_balance* buy_ratio)
                print(f"매수 주문이 실행되었습니다. 양: {krw_balance * buy_ratio}")
            elif sell_condition(current_price, ma):
                upbit.sell_market_order(ticker, balance * sell_ratio)
                print(f"매도 주문이 실행되었습니다. 양: {balance * sell_ratio}")

            # 일정 간격으로 반복 실행
            time.sleep(60)  # 5분 간격으로 실행

        except Exception as e:
            print(f"에러 발생: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
    import time