# RAN_testing
let's first understand what 5G NR Random Access (RA) is.

According to 3gpp specification 38.321 5G NR Random Access is a crucial process that enables User Equipment (UE) to establish an initial connection with the gNB (gNodeB) for communication. This process plays a key role in:

Initial access – When a device first connects to the network.
Handover – When a device moves between different base stations.
Synchronization recovery – When a device loses connection and needs to reconnect.
To better understand this concept, let’s use an analogy:

Imagine you are entering a large event, such as a concert or a conference. You cannot simply walk in; you first need to check in at the entrance. Similarly, 5G NR Random Access acts as a check-in process for mobile devices, ensuring they gain proper access to the network.


Our project focuses on automating the performance testing of the 5G NR Random Access procedure using the NS-3.42 network simulator. In this presentation, we will cover:

The methodology used for automation.
The key performance metrics measured.
The insights gained from our automated testing process.
Objective of the Project
The main goal of this project is to develop an automated and repeatable testing framework for evaluating the performance of the 5G NR Random Access procedure under different network conditions, mobility scenarios, and parameter settings. This automation helps to:

Identify potential bottlenecks in the RA process.
Optimize network configurations for improved performance.
Provide comprehensive and reliable data for analysis.
By leveraging 3GPP standards and fixing implementation errors, we ensure our automated framework aligns with real-world 5G deployment requirements.

key matrix used:-
3GPP Definition:
PRACH Success Rate is the percentage of successful random access attempts compared to the total attempts made by all UEs.
3GPP Definition:
Collision Probability is the percentage of PRACH attempts where multiple UEs select the same preamble, leading to a failure.
3GPP Definition:
Access Delay is the average time between the start of a PRACH attempt and the successful completion of the random access process.
 3GPP Definition:
Retransmissions refer to the number of times a UE must retry the random access process after a failure (collision or timeout).
