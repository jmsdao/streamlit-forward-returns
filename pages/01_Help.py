import streamlit as st

# ----------------------------------------------------------------------------
# --- Sidebar ---
# ----------------------------------------------------------------------------
st.sidebar.markdown("""
## Jump to Section

<ul class="contents">
   <li><a class="contents-el" href="#how-do-i-read-this-plot">How do I read this plot?</a></li>
   <li><a class="contents-el" href="#what-is-cumulative-vs-annualized-returns">What is cumulative vs. annualized returns?</a></li>
   <li><a class="contents-el" href="#what-is-percent-vs-log-returns">What is percent vs. log returns?</a></li>
   <li><a class="contents-el" href="#formulas-for-the-4-return-metrics">Formulas for the 4 return metrics</a></li>
</ul>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# --- Main Content ---
# ----------------------------------------------------------------------------
st.markdown(
r"""
### How do I read this plot?
The Y-axis is the return of a particular stock if it's held for a duration of
the defined holding period.  
The X-axis is the starting date of the holding period.

You can hover over data points in the plot to see more details.

I occasionally call it a forward return because it's the return you'd get if you
purchased an asset on a particular past date and "looked forward" by a particular
holding period.


### What is cumulative vs. annualized returns?
The cumulative return is simply the return you'd get from an asset by comparing
its start and end price, ignoring how long the holding period is. The annualized
return is the return you'd need per year for the equivalent cumulative return.
In other words, annualized return normalizes the cumulative return by the holding
period. This leads to more fair comparisons of forward returns with different
holding periods.

**Example 1**  
If a stock went from \$100 to \$121 over a period of 2 years, its
cumulative percent return is 21%, but it's annualized percent return is 10%.
This is because getting a 10% return each year for 2 years would be equivalent
to getting a 21% return over 2 years (1.1 * 1.1 = 1.21).

**Example 2**  
If a stock went from \$100 to \$110 over a period of half a year, its cumulative
percent return is 10%, but it's annualized percent return is 21%. This is because
if you got a 10% return in half a year, then hypothetically got another 10% in
another half a year, your cumulative return for that full year would be 21%
(1.1 * 1.1 = 1.21).


### What is percent vs. log returns?
Percent return is the percentage difference between the start and end price of an
asset, with the start price in the denominator. Log return is the logarithm of the
ratio of the start and end price, with the start price in the denominator.

**Example**  
If an asset goes from \$100 to \$125, its percent return is 25% and its log return
would be about 0.223. Consequently, if an asset goes from \$125 to \$100, its
percent return would be -20% and its log return would be about -0.233.

**Why use log returns?**  
From the example above, you can see that log returns make gains and losses numerically
symmetrical. If you suffered a -50% percent return (-0.693 log return), you'd need
a 100% return (0.693 log return) to get back to the inital price.

While log returns are less intuitive for understanding a price movement, it allows for
a more fair visual comparison of gains and losses.


### Formulas for the 4 return metrics
$t$ : start date of the holding period  
$n$ : length of holding period in years  
$p_{t}$ : price of an asset at time $t$ (start price)  
$p_{t+n}$ : price of an asset at time $t+n$ (end price)

##### $$Cumulative Percent Return = \frac{p_{t+n}}{p_{t}} - 1$$

##### $$Annualized Percent Return = (\frac{p_{t+n}}{p_{t}})^{\frac{1}{n}} - 1$$

##### $$Cumulative Log Return = \ln{(\frac{p_{t+n}}{p_{t}})}$$

##### $$Annualized Log Return = \frac{1}{n}\ln{(\frac{p_{t+n}}{p_{t}})}$$


"""
)
