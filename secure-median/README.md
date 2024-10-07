# A Secure Median Implementation for the Federated Secure Computing Architecture

## Authors: Christian Goelz, Solveig Vieluf, Hendrik Ballhausen

This repository contains the client-side code for testing the secure median algorithm implemented within the Federated Secure Computing framework and SIMON. The related publication "A Secure Median Implementation for the Federated Secure
Computing Architecture" can be found [here](https://doi.org/10.3390/app14177891). Below are detailed instructions for running the code in a local deployment (Windows users should use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)).

- [Installation](#installation)
- [Run Benchmarking](#run-benchmarking)
  - [Random Numbers](#random-numbers)
  - [Breast Cancer](#breast-cancer)
  - [Heart Disease](#heart-disease)

## Installation

To install the required packages and dependencies, follow the steps below:

### Server Setup

```sh
pip install federatedsecure-server
pip install federatedsecure-simon
pip install connexion[flask,uvicorn,swagger-ui]
git clone https://github.com/federatedsecure/webserver-connexion

```

### Client Setup:
```sh
pip install federatedsecure-client
pip install pandas
```

## Run Benchmarking
### Random numbers
To test the implementation for two clients in a local deployment, where each client runs its own server to calculate the median of arrays of random numbers, follow these steps:
1. Start two servers on localhost, running on ports `55500` and `55501` (you can use different ports if needed):
```sh
cd webserver-connexion/src
python __main__.py port=55500 &
python __main__.py port=55501 &
```
2. Configure the servers in the servers.cfg file:
```
[UUID]
uuid=29854ef6-055d-4044-baf4-1378530ea037

[SERVER1]
host = http://127.0.0.1
port = 55500

[SERVER2]
host = http://127.0.0.1
port = 55501
```
* UUID refers to a unique identifier (you can use the provided one or generate a new UUID).
* The host is set to `http://127.0.0.1`, indicating the servers are running on localhost.
* The ports are set to `55500` and `55501`, corresponding to the servers' ports we specified previously.

3. Run the benchmarking script (`benchmark_rand.py`) for each client in parallel. The script requires three arguments:
- **Arg1**: The client index (e.g., `0` for client 1 and `1` for client 2).
- **Arg2**: The upper range of random numbers (e.g., `100` generates numbers in the range of `1` to `100`).
- **Arg3**: The number of elements for each party (e.g., `100` generates 100 numbers per party).

To run the benchmarking for 200 inputs (100 per client within the range of `1` to `100`) in a new terminal window run:

```sh
python src/benchmark_rand.py 0 100 100 &
python src/benchmark_rand.py 1 100 100 
```

Note: To increase the number of clients, start additional servers and add them to the `servers.cfg` file. 

### Breast Cancer
1. Start two servers as outlined in the previous section.
2. Add both servers to the `servers.cfg` file.
3. Run the benchmarking script (`benchmark_ucml.py`) with the following arguments:
    - **Arg1**: The index of the client (e.g., `0` or `1`).
    - **Arg2**: The filename corresponding to the client (e.g., `breast_cancer_wisconsin_diagnostic_1.csv`).
    - **Arg3**: The column over which to calculate the median (e.g., `radius1`).

```sh
python src/benchmark_ucml.py 0 data/breast_cancer_wisconsin_diagnostic_1.csv radius1 &
python src/benchmark_ucml.py 1 data/breast_cancer_wisconsin_diagnostic_2.csv radius1 
```

### Heart disease
1. Start four servers as described in the previous section.
2. Add all four servers to the `servers.cfg` file.
3. Run the benchmarking script (`benchmark_ucml.py`) with the following arguments:
    - **Arg1**: The index of the client (e.g., `0`, `1`, `2`, or `3`).
    - **Arg2**: The filename corresponding to the client (e.g., `heart_disease_cleveland.csv`).
    - **Arg3**: The column over which to calculate the median (e.g., `age`).

```sh
python src/benchmark_ucml.py 0 heart_disease_cleveland.csv age &
python src/benchmark_ucml.py 1 heart_disease_hungarian.csv age &
python src/benchmark_ucml.py 2 heart_disease_switzerland.csv age &
python src/benchmark_ucml.py 3 heart_disease_va.csv age 
```
