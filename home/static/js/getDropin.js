function showInfo() {
  document.getElementById("customer-info").removeAttribute("hidden");
  var butinfo = document.getElementById("b_compra");
  butinfo.setAttribute("onclick", "javascript:compraclick()");
  butinfo.setAttribute("style", "font-size:rem;");
  butinfo.innerHTML = "Invia informazioni e compra";
}
function compraclick() {
  inputs = document.getElementsByTagName('input');
  for (index = 0; index < inputs.length; ++index) {
    if (inputs[index].value != "") {
      continue;
    }
    else {
      alert("inserisci bene tutte le informazioni per la spedizione");
      return -1;
    }
  }
  dropinCreate();
}

function checkSpedizione() {

  dropinCreate();
}

$(document).ready(function () {
  var button = document.querySelector('#submit-button');
  var bcompra = document.querySelector('#b_compra');
  $(bcompra).click(function () {
    showInfo();
  })
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }




});
function dropinCreate() {
  includeHTML();
  var pf = document.getElementById("paypalform")
  //pf.removeAttribute("hidden");
}

function includeHTML() {
  var z, i, elmnt, file, xhttp;
  /* Loop through a collection of all HTML elements: */
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    /*search for elements with a certain atrribute:*/
    file = elmnt.getAttribute("w3-include-html");
    if (file) {
      /* Make an HTTP request using the attribute value as the file name: */
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) { elmnt.innerHTML = this.responseText; }
          if (this.status == 404) { elmnt.innerHTML = "Page not found."; }
          /* Remove the attribute, and call this function once more: */
          elmnt.removeAttribute("w3-include-html");
          includeHTML();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      /* Exit the function: */
      return;
    }
  }
}