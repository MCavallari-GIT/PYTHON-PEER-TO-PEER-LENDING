# Python-peer-to-peer-lending
The goal of the project is to build a simplified and proof-of-concept software application for peer-to-peer lending or social lending, which is a service managed by an internet company that acts as a financial intermediary for matching money lenders and borrowers with a reduced overhead comparing with traditional banking systems. We assume that the software will be used by some operator of the financial intermediary company. The software is composed of a user interface and business logic part written in Python and an SQL database management system to store the data.


## Application domain model
We suppose a borrower can request a loan amount declaring a certain interest rate cap (s)he is willing to bear. The lenders can bid for offering a certain amount of money competing for the lowest interest rate as in the reverse auctions.
At any moment the borrowers can apply for loan requests and the lenders can propose their bids. As soon as one request, at least, can be matched with some bid(s) according to the following criteria, the loan request and the matched bid(s) are bound to a contractual agreement.
A loan request can be matched to one or more lender’s bids when: there is/are available (namely unbound) bid(s) whose total amount is above or equal to the request’s amount and the offered interest rate in each of those bids is not greater than the interest rate cap of the loan request.

In order to minimize the loan interest for the borrower, the matching criterion consists in selecting among those bids meeting the conditions above in increasing order of interest rate (i.e. the lower the rate, the higher the priority) until reaching the requested amount for the loan. It might be enough to use only a portion of
the last selected bid to reach the requested amount. The loan request of the borrower and the money bids of the lenders enter into a loan contractual agreement, which is characterized by these information among others: a unique loan contract ID, the matched loan request and bids, the loan amount and the weighted average interest rate. For sake of simplicity, weights are determined by the amounts used from the bids.

## Example
Suppose we have one request of € 100,000 loan with a 4% interest rate cap, and four bids:
1) € 40,000 at 2% interest rate
2) € 75,000 at 1.5% interest rate
3) € 60,000 at 5% interest rate
4) € 50,000 at 3.5% interest rate

The loan request could be potentially matched with 1), 2) and 4), but because of the above order criterion it will be actually matched with 1) and with 2) by a portion, € 60,000, only. The formed agreement will contractually bind the loan request to the selected bids 1) and 2) with a (weighted average) interest rate of (2 ⋅ 40000 + 1.5 ⋅ 60000)/100000 = 1.7 percent).

The selected bids, that entered into a contractual agreement, cannot be reused for other matchings.
At any moment, if more than one loan request can be matched, the choice of the one to be actually matched first can be arbitrary (specify the choice followed by your project in the report document).

## User interaction
The financial intermediary operator can interact with the system with regular operations
that are intended to manage loan requests and bids:
- Record a loan request
- Record a bid
- List all unmatched loan requests
- List all unmatched bids
- Cancel a loan request
- Cancel a bid

Moreover, the software can fulfill the following simple summary operations:

- Show the number of contractually agreed loans
- Show the number of contractually agreed loans having a certain amount at most
- Show the total amount of all contractually agreed loans
- Show the overall weighted average interest rate among all contractually agreed loans
- List the information of all contractually agreed loans

The program shall show an error (as specified later on) in case any of the operations above cannot be accomplished (e.g. cancelling a non-existing request, recording a negative amount bid, …).

## Program specification
The Python program, that communicates wih the DBMS storing the data, shall
repeatedly: 
1) output only the string "> " (greater than symbol followed by a space character) in a line, and
2) wait for a user's command as input, 
3) execute one-by-one all possible matchings according to criteria
described above, and then 
4) possibly output the corresponding outcome if any, according to the following specifications:

## Command Syntax Description
1) L a c -->Record a loan request for the amount a with an interest rate cap of c %.
Example commands:
L 100000 2
L 30000 1.5

2) B a r -->Record a lender's bid by an amount a with an interest rate of r %.
Example commands:
B 30000 1.25
B 45000 3

3)UL -->List every unmatched loan request in the format:
a c, where a is the amount and c is the rate cap.
Example output:
30000 1.5
100000 2

4) UB -->List every unmatched bid in the format: a r, where a is the amount and r % is
the interest rate.
Example output:
30000 1.25
45000 3

5) CL a c -->Cancel a loan request corresponding to amount a and rate cap c %.

6) CB a r -->Cancel a bid corresponding to amount a and interest rate r %.

7) NA -->Show the number of contractually agreed loans.
Example output:
3

8) NG a -->Show the number of contractually agreed loans having an amount a at most.
Example output:
0

9) T -->Show the total amount of all contractually agreed loans.
Example output:
1500000

10) W -->Show the overall weighted average interest rate among all contractually agreed
loans
Example output:
1.3251

11) A --> List every contractually agreed loan in the format: a r, where a is the loan amount
and r % is the interest rate contractually agreed to the borrower.
Example output:
100000 1.12
30000 0.894

12) X -->Exit (close) the program
