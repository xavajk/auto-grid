## Introduction

Climate change drives extreme weather conditions with wildfires, hurricanes, and floods, triggering major outages and instabilities in the electric power grid in the US and elsewhere.

Microgrids have emerged as viable sources of reliable, resilient, and renewable electric power produced from carbon-free natural resources. They are being installed worldwide in different shapes and sizes and in urban and rural areas not only as reliable power sources but also as means to reduce carbon emissions and combat climate change.

## Microgrid

A microgrid incorporates a generation mix of intermittent solar, wind, and/or biogas to produce electric power to meet local demand with or without energy storage. It can operate as an islanded or a grid-connected power system.

## SCADA

Supervisory Control and Data Acquisition (SCADA) systems have inherently been used to remotely monitor, supervise, and control the grid components as a means to operate the electric power grid of utilities such as PG&E efficiently and reliably. The conventional SCADA, however, is expensive to customize and deploy for microgrids. The intermittent nature of renewables requires more sophisticated control platforms and intelligent software to maintain the generation load balance and to keep frequency and voltage levels within limits in real-time when the sun stops shining, or the wind stops blowing.

scada-agents is about developing a multi-agent SCADA system to manage and operate microgrids securely. Here, the agents are built to autonomously manage and operate components of the generation mix, end-use demand, and storage batteries and control and coordinate the other agents at the microgrid.

## Generation

- One or more PhotoVoltaic Panel to produce renewable solar energy
- One or more Wind Turbine (will not be considered yet)
- One or more BioGas (will not be considered yet)
- One or more Hydro Generator (will not be considered yet)
- One or more Non-renewable Generator such as diesel generators or gas turbines to produce non-renewable energy when sufficient energy is not available from other sources

## Demand

- Residential Home
- Non-Residential Building

## Storage

- Storage Batteries to store energy when there is excess of energy on the microgrid and to compensate for the shortage of energy when needed

## Control

- Circuit Breakers for switching on/off generation or load instances from the grid
- Voltage-controlled Converters
- Point of Common Coupling

## Agents

An intelligent software that can be designed and implemented to autonomously manage and operate the microgrid's components (i.e., generation, storage, control, load) and actively communicate and coordinate with the other microgrid agents as a comprehensive and integrated real-time microgrid SCADA.

We use the Agent Class in SPADE, which has the following properties: .....

In the implementation of SCADA, the following main types of agents are defined and inherit the properties of the Agent class in SPADE:

- Power Generation Agent: It represents a potential power generation resource, mainly a photovoltaic, wind, biogas, hydro, non-renewable generation, or a combination of one or more resources. It interfaces with the human operator using a web or mobile application by which it is possible to monitor and operate the physical power generator and perceive notifications by means of a subscription protocol.
- Power Demand Agent: It represents a power load representing RH, NB, or a combination of one or more of these buildings that need electricity for lighting, appliances, heating, air conditioning, or EV charging. It operates a power demand management system and interfaces with a human operator using a web or mobile application by which it is possible to monitor and manage power consumption.
- Storage Battery Agent:
- Device Control Agent:
- Tertiary Control Agent: This agent is in charge of computing day-ahead and hour-ahead optimal power flow schedules. The schedules represent the amount of electric power (active and reactive) at the generation and demand resources and the flow of power over the transmission lines of the power network.
- Secondary Control Agent: This agent is in charge of maintaining the generation-load balance, tuning the transition console parameters, and controlling the voltage and frequency deviations.
- Primary Control Agent: This agent is in charge of the real-time control of the microgrid, operating its voltage-control convertors and maintaining voltage and frequency stability.

## Model

We give details of the generic microgrid prototype as follows:

- Microgrid network using PyPSA package with n_busses interconnected with transmission lines that have r+jx impedances.
- Solar and diesel generators are added to one or more network buses.
- One or more loads (power demand) added to one or more network buses.
