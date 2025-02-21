using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MyRCCar
{
    public partial class Form1 : Form
    {
        private TcpListener listener;
        private TcpClient client;
        private NetworkStream stream;
        private Thread serverThread;
        private Thread receiveThread;
        private bool isRunning = false;

        public Form1()
        {
            InitializeComponent();
            tbIP.Text = "192.168.0.145";
            lblResult.Text = "";

            CheckForIllegalCrossThreadCalls = false;
        }

        private void btnConnect_Click(object sender, EventArgs e)
        {
            if (isRunning)
            {
                WriteLog("서버가 이미 실행 중입니다.");
                return;
            }

            string ip = tbIP.Text;
            string port = tbPort.Text;

            if(!IPAddress.TryParse(ip, out IPAddress iPAddress) || !int.TryParse(port, out int portt))
            {
                WriteLog("올바른 IP와 포트 번호를 입력하세요."); 
                return;
            }

            serverThread = new Thread(()=>StartServer(iPAddress, portt));
            serverThread.IsBackground = true;
            serverThread.Start();
        }

        private void StartServer(IPAddress ip, int port)
        {
            try
            {
                listener = new TcpListener(ip, port);
                listener.Start();
                isRunning = true;
                WriteLog($"서버 시작 : {ip}:{port}");
                WriteLog("클라이언트 연결 대기 중...");

                client = listener.AcceptTcpClient();
                stream = client.GetStream();
                WriteLog("클라이언트가 연결되었습니다.");
                lblResult.Text = "Waiting...";
            }
            catch (Exception ex)
            {
                WriteLog($"서버 오류 : {ex.Message}");
                lblResult.Text = "Error";
            }
        }



        private void btnGo_Click(object sender, EventArgs e)
        {
            SendMessage("GO");
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            SendMessage("STOP");
        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            SendMessage("BACK");
        }

        private void btnLeft_Click(object sender, EventArgs e)
        {
            SendMessage("LEFT");
        }

        private void btnRight_Click(object sender, EventArgs e)
        {
            SendMessage("RIGHT");
        }

        private void SendMessage(string message)
        {
            if (client == null || !client.Connected)
            {
                WriteLog("클라이언트가 연결되지 않았습니다");
                return;
            }

            try
            {
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                stream.Write(buffer, 0, buffer.Length);
                WriteLog($"Send [{message}]");
            }
            catch (Exception ex)
            {
                WriteLog($"전송 오류 : {ex.Message}");
            }
        }

        private void WriteLog(string log)
        {
            string timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            rtbLog.AppendText($"{timestamp} : {log}\n");
        }
    }
}
