# Modeling and optimization of serving customer flow using the example of coffee vending machines in an office complex

#### *Remark*: This project does not aim to be a scientific research tool or anything similar; it is simply a personal study project that I created to enhance my knowledge in the Theory of Stochastic Processes and Optimization.

## Quick briefing
- Let's imagine a situation in which there is an “entrepreneur” who wants to equip a certain service area in an office complex with n number of coffee machines.
- He wants to arrange it in such a way that the flow of customers is close to constant, i.e., queues are minimal, and there are no extra machines that would stand idle.
- So far, this zone consists of m machines.
- Entrepreneurs can do their own research. For a certain period of time, for example, 30 days, every day from 8 to 18, he will monitor the intensity of the flow of customers every hour.
    - Day 1:
    - 8:00 - 9:00 - 40 customers
    - 9:00 - 10:00 - 55 customers
    - ...
    - Day 2:
    - 8:00 - 9:00 - 35 clients
    - 9:00 - 10:00 - 40 clients
    - ...
- Thus, samples of 30 values for each hour will be obtained. Having determined the sample mean and variance, he will be able to determine the spread of values relative to the sample mean (mathematical expectation) and, accordingly, draw certain conclusions about whether this sample is representative. If so, he will group the sample means (mathematical expectations) related to each hour. They will correspond to the parameters of the lambda Poisson distribution.
- Having received this data, he will be able to run this program and get the optimal number of coffee machines to equip his self-service area.

## Math behind Implementation


### Fundamental things
To generate the events “customer arrived at the queue” and “customer received his order”, generated values of a random variable from the Poisson distribution with the corresponding lambda parameters are used. The lambda parameter for generating the “Customer arrived at the queue” event is taken from the time-dependent parameters entered by the user. And the lambda parameter for generating the “Customer has received his order” event is constant and does not depend on time in the simulation. The flow of such events is called a Poisson flow.

- A Poisson flow is a mathematical model of a random process where events occur independently of each other and with a constant average intensity in time or space. This process describes the number of events that occur during a certain time interval or in a certain area. A Poisson event stream is characterized by the fact that the number of events occurring in a fixed time interval has a **Poisson distribution with a lambda parameter**. The lambda parameter is the average number of events that occurred over a certain period of time. That is, the intensity of events.
- The probability of occurrence of n events in a period of time t is:

    $$P(N(t) = n) = \frac{{e^{-\lambda t} \cdot (\lambda t)^n}}{{n!}}$$


- In such a stream, the time intervals between events are random variables with **exponential distribution** with the inverse parameter 1/λ corresponding to the stream.
    - The probability of one such interval is determined by the function of this distribution: <br/>
    $$P(X \leq x) = 1 - e^{-\lambda x}$$

    

### Methods used to process data in the metrics class.
- To obtain the average customer waiting time, the mathematical expectation (sample average) of the sample gradually formed during the simulation from the waiting time of each customer is found. The waiting time for each customer is formed as the sum of the time spent in the queue + the service time.
- To obtain the average waiting time for each of the machines, the mathematical expectation (sample mean) of the sample gradually formed during the simulation from the waiting time of each machine per customer is found

### Methods and algorithms used for optimization.

- To optimize the n number of coffee machines in order to minimize the average time a customer waits for his order (including the queue, of course) and the average time a machine waits for a customer (during idle time), the objective function will be minimized: <br/>
    $$f(x(n))=αx_1(n) +βx_2(n)$$ </br>
    $$0 < n < n^\*$$ </br>
    $$n ∈ Z$$ </br>
    $$n* ∈ Z$$ </br>
    - where the weighting factor α denotes the importance of minimizing the average customer waiting time, and β denotes the average machine downtime. By default, they are equal to one, but the user can enter their own values of alpha and beta to obtain a suitable objective function.

- In the software implementation, to obtain the optimal value of the parameter n in the range from 1 to n\*, samples of 50 required metric values are sequentially built - the average customer waiting time and the average waiting time of machines (if there are several machines, the average value is taken) for $n=1, ..., n^\*-1$. That is, we get 2 samples of 50 values at each iteration. The total number of such samples is $2(n^\*-1)$. After that, the sample means of these samples are found, which correspond to the functions $x_1(n)$ and $x_2(n)$.
  
- Substituting these values into the objective function, we will find the value of n at which the function will be minimal using the minimum search algorithm.
  
- As a result, the optimal solution to the problem of minimizing this objective function will be obtained. That is, the optimal n number of coffee machines will be found.


## Implementation

### List of tools used for implementation (modules, libraries).

  
- The `simpy` library was used to simulate the environment. With the help of its `Environment` class, the environment in which the simulation of the process of variable customer flow over time was carried out was modeled.
  
- To simulate the flow of customers, the library simpy was used, again, to simulate the flow of customers. Namely, the `Environment.timeout()` method, which recorded the time of the occurrence of the customer appearance event (a new customer joins the queue), the event - the customer stands at the vending machine to place an order and the event - the customer received his order.
  
- Using the numpy library method `random.exponential(λ)`, the time of the event - a new customer joins the queue - is generated. Depending on the time, the parameter λ, which generates the time of occurrence of this event in the simulated environment, will correspond to the parameter entered by the user.
  
- Customers are queued for many machines at once, i.e. if one of the n number of machines is released, it is immediately taken by the first person in the queue. If the client has a choice of which free slot machine to use, it will be generated as a random number using the `numpy.random.randomint` method within the range 

