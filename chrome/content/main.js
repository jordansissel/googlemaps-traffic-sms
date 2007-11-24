var traffic = {
  onload: function(e) {
    //dump("alive\n");
    this.init = true;
    var nsCommandLine = window.arguments[0];
    nsCommandLine = nsCommandLine.QueryInterface(Components.interfaces.nsICommandLine);
    this.url = nsCommandLine.handleFlagWithParam("url", false);
    this.url = this.url || "http://www.google.com";

    this.title = nsCommandLine.handleFlagWithParam("title", false);

    document.getElementById("main-window").setAttribute("title", this.title);
    //dump("Setting title: " + this.title + "\n")

    this.browser = document.getElementById("main-browser");
    this.browser.loadURI(this.url, null, null);
  },
};

window.addEventListener("load", traffic.onload, false);
