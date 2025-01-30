import art

print(art.logo)

def find_highest_bidder(bidding_dictionary):
    highest_bid = 0
    winner = ""
    for bidder, bid_amount in bidding_dictionary.items():
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder
    return winner, highest_bid

def collect_bids():
    bids = {}
    while True:
        name = input("What is your name? : ")
        price = float(input("What is your bid for this item? : $"))
        bids[name] = price
        
        should_continue = input("Are there any other bidders? 'yes' or 'no': ").lower()
        if should_continue == "no":
            break
        elif should_continue == "yes":
            print("\n" * 20)
    
    return bids

def main():
    bids = collect_bids()
    winner, highest_bid = find_highest_bidder(bids)
    
    if winner:
        print(f"The winner is {winner} with a bid of ${highest_bid:.2f}")
    else:
        print("No bids were placed.")

if __name__ == "__main__":
    main()
