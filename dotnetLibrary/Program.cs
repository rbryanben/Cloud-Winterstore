using System;
using System.Net.Http;

namespace dotnetLibrary
{
    class Program
    {
        static void Main(string[] args)
        {
            WinterstoreConnect hello = new WinterstoreConnect("http://127.0.0.1/8000")
            hello.checkGateway()
        }
    }

    public class WinterstoreConnect() {

        //class attributes
        private HttpClient client = new HttpClient();
        private string serverURL ;
        
        public WinterstoreConnect(string serverURL) {
            this.serverURL = serverURL ;
        }

        //gateway check 
        public void checkGateway() {
            try {
                HttpResponceMessage responce = await this.client.GetAsync(this.serverURL + "/api/gateway/");
                responce.EnsureSuccessStatusCode();
                string responceBody = await response.Content.ReadAsStringAsync();

                Console.WriteLine(responceBody)
            }
            catch (Exception e){
                Console.WriteLine(e.Message)
            }
        }
    }
}
