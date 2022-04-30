#include <fstream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/netanim-module.h"

using namespace ns3;

class MyApp : public Application{
	
public:
	MyApp ();
	virtual ~MyApp ();

	/**
	 * Register this type.
	 * \return The TypeId.
	 */
	static TypeId GetTypeId (void);
	void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
	virtual void StartApplication (void);
	virtual void StopApplication (void);

	void ScheduleTx (void);
	void SendPacket (void);

	Ptr<Socket>     m_socket;
	Address         m_peer;
	uint32_t        m_packetSize;
	uint32_t        m_nPackets;
	DataRate        m_dataRate;
	EventId         m_sendEvent;
	bool            m_running;
	uint32_t        m_packetsSent;
};

MyApp::MyApp ()
  : m_socket (0),
    m_peer (),
    m_packetSize (0),
    m_nPackets (0),
    m_dataRate (0),
    m_sendEvent (),
    m_running (false),
    m_packetsSent (0)
{
}

MyApp::~MyApp (){
	m_socket = 0;
}

/* static */
TypeId MyApp::GetTypeId (void) {

	static TypeId tid = TypeId ("MyApp")
		.SetParent<Application> ()
		.SetGroupName ("Tutorial")
		.AddConstructor<MyApp> ()
		;
	return tid;
}

void MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate){

	m_socket = socket;
	m_peer = address;
	m_packetSize = packetSize;
	m_nPackets = nPackets;
	m_dataRate = dataRate;
}

void MyApp::StartApplication (void){

	m_running = true;
	m_packetsSent = 0;
	m_socket->Bind ();
	m_socket->Connect (m_peer);
	SendPacket ();
}

void MyApp::StopApplication (void){

	m_running = false;

	if (m_sendEvent.IsRunning ()){
		Simulator::Cancel (m_sendEvent);
	}

	if (m_socket){
		m_socket->Close ();
	}
}

void MyApp::SendPacket (void){

	Ptr<Packet> packet = Create<Packet> (m_packetSize);
	m_socket->Send (packet);

	if (++m_packetsSent < m_nPackets){
		ScheduleTx ();
	}
}

void MyApp::ScheduleTx (void) {

	if (m_running){

		Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
		m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
	}
}

static void CwndChange (Ptr<OutputStreamWrapper> stream, uint16_t connectionNo, uint32_t oldCwnd, uint32_t newCwnd){

	NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" <<connectionNo << "\t"<< newCwnd);
	*stream->GetStream () <<Simulator::Now ().GetSeconds () << "\t" <<connectionNo << "\t"<< newCwnd << std::endl;
}

static void RxDrop (Ptr<OutputStreamWrapper> stream, Ptr<PcapFileWrapper> file, Ptr<const Packet> p){

	NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
	*stream->GetStream () <<"RxDrop at " << Simulator::Now ().GetSeconds ()<< std::endl;
	file->Write (Simulator::Now (), p);
}

std::string Connection1;
std::string Connection2;
std::string Connection3;
int config;


NS_LOG_COMPONENT_DEFINE ("QuesThird");

void setConnection(uint16_t sinkPort, NodeContainer nodes, Ipv4InterfaceContainer interfaces, uint32_t startTime, 
				   uint32_t finishTime, uint16_t sourceNo, NetDeviceContainer devices, Ptr<OutputStreamWrapper> stream,
				   Ptr<PcapFileWrapper> file, uint16_t connectionNo, std::string connectionType){
	
	Address sinkAddress (InetSocketAddress (interfaces.GetAddress (1), sinkPort));
	PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
	ApplicationContainer sinkApps = packetSinkHelper.Install (nodes.Get (2));
	sinkApps.Start (Seconds (0.));
	sinkApps.Stop (Seconds (30.));

	TypeId tid = TypeId::LookupByName (connectionType);
	std::stringstream nodeId;
	nodeId << nodes.Get (sourceNo)->GetId ();
	std::string specificNode = "/NodeList/" + nodeId.str () + "/$ns3::TcpL4Protocol/SocketType";
	Config::Set (specificNode, TypeIdValue (tid));

	Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (nodes.Get (sourceNo), TcpSocketFactory::GetTypeId ());

	Ptr<MyApp> app = CreateObject<MyApp> ();
	app->Setup (ns3TcpSocket, sinkAddress, 3000, 100000, DataRate ("1.5Mbps"));
	nodes.Get (sourceNo)->AddApplication (app);
	app->SetStartTime (Seconds (startTime));
	app->SetStopTime (Seconds (finishTime));

	ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeBoundCallback (&CwndChange, stream, connectionNo));
    
}

void Run(){

    NodeContainer nodes;
    nodes.Create(3);

    PointToPointHelper link13;
    link13.SetDeviceAttribute ("DataRate",StringValue("10Mbps"));
    link13.SetChannelAttribute ("Delay",StringValue("3ms"));

    PointToPointHelper link23;
    link23.SetDeviceAttribute ("DataRate", StringValue("9Mbps"));
    link23.SetChannelAttribute ("Delay", StringValue("3ms"));

    NetDeviceContainer devices1 = link13.Install (nodes.Get(0),nodes.Get(2));
	NetDeviceContainer devices2 = link13.Install (nodes.Get(1),nodes.Get(2));

    InternetStackHelper stack;
	stack.Install (nodes);

	Ptr<RateErrorModel> em1 = CreateObject<RateErrorModel> ();
	em1->SetAttribute ("ErrorRate", DoubleValue (0.00001));

	Ptr<RateErrorModel> em2 = CreateObject<RateErrorModel> ();
	em2->SetAttribute ("ErrorRate", DoubleValue (0.00001));

	devices1.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em1));
	devices2.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em2));

    Ipv4AddressHelper address1;
	address1.SetBase ("10.1.1.0", "255.255.255.0");
	Ipv4InterfaceContainer interfaces1 = address1.Assign (devices1);

	Ipv4AddressHelper address2;
	address2.SetBase ("192.178.1.0", "255.255.255.0");
	Ipv4InterfaceContainer interfaces2 = address2.Assign (devices2);
	
	AsciiTraceHelper asciiTraceHelper;
	Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream ("Third"+ std::to_string(config) + "-out.cwnd");
	PcapHelper pcapHelper;
	Ptr<PcapFileWrapper> file = pcapHelper.CreateFile ("Third.pcap", std::ios::out, PcapHelper::DLT_PPP);

	devices1.Get (1)->TraceConnectWithoutContext ("PhyRxDrop", MakeBoundCallback (&RxDrop, stream, file));
	devices2.Get (1)->TraceConnectWithoutContext ("PhyRxDrop", MakeBoundCallback (&RxDrop, stream, file));

    setConnection(8080,nodes,interfaces1,1,20,0,devices1,stream,file,1,Connection1);
	setConnection(8090,nodes,interfaces1,5,25,0,devices1,stream,file,2,Connection2);
	setConnection(9000,nodes,interfaces2,15,30,1,devices2,stream,file,3,Connection3);
    
	Simulator::Stop (Seconds (30));
	Simulator::Run ();
	Simulator::Destroy ();
}



int main (int argc, char *argv[]){

	CommandLine cmd;
	cmd.AddValue("C", "Configuration", config);
	cmd.Parse (argc, argv);

	switch (config)
	{
	case 1:
		Connection1 = "ns3::TcpNewReno";
		Connection2 = "ns3::TcpNewReno";
		Connection3 = "ns3::TcpNewReno";
		break;

	case 2:
		Connection1 = "ns3::TcpNewReno";
		Connection2 = "ns3::TcpNewReno";
		Connection3 = "ns3::TcpNewRenoCSE";
		break;

	case 3:
		Connection1 = "ns3::TcpNewRenoCSE";
		Connection2 = "ns3::TcpNewRenoCSE";
		Connection3 = "ns3::TcpNewRenoCSE";
		break;
	
	default:
		std::cout << "INVALID CONFIGURATION" << std::endl;
		return -1;
	}


	Run();

	return 0;
}

