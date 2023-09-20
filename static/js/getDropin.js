
var binfo;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {
  var customerInfo, butinfo, butcheckinfo;
  butinfo = document.querySelector('#submitBtnnone');
  butcheckinfo = document.querySelector('#checkinfo');
  customerInfo = document.querySelector('#customer-info');
  $('#submitBtnnone').click(function () {
    customerInfo.removeAttribute('hidden');
    butinfo.setAttribute('hidden', 'hidden');
    butcheckinfo.removeAttribute('hidden');
    butcheckinfo.setAttribute("visibility", "visible");
  });

  $('#checkinfo').click(function () {
    var funct = verificaInfo();
  })

  function verificaInfo() {
    inputs = document.getElementsByTagName('input');
    textarea = document.getElementById("infoerichieste");
    for (index = 0; index < inputs.length; ++index) {
      if (inputs[index].value != "") {
        if (inputs[index].id == "inome") {
          var inome = inputs[index].value;
        }
        else if (inputs[index].id == "icognome") {
          var icognome = inputs[index].value;
        }
        else if (inputs[index].id == "ivia") {
          var ivia = inputs[index].value;
        }
        else if (inputs[index].id == "icivico") {
          var icivico = inputs[index].value;
        }
        else if (inputs[index].id == "itelefono") {
          var itelefono = inputs[index].value;
        }
        else if (inputs[index].id == "icitta") {
          var icitta = inputs[index].value;
        }
        else if (inputs[index].id == "icap") {
          var icap = inputs[index].value;
        }
        var infoerichieste = ""
        if (textarea.value !== "") {
          try {
            infoerichieste = textarea.value;
          }
          catch {
            infoerichieste = ""
          }
        }
        continue;
      }
      else {
        alert("inserisci bene tutte le informazioni per la spedizione");
        return -1;
      }
    }
    var prodotto = productid;
    var datainfo = JSON.stringify({
      'productid': productid, 'nomeuser': inome, 'cognome': icognome, 'citta': icitta, 'cap': icap, 'telefono': itelefono,
      'infoerichieste': infoerichieste, 'via': ivia, 'civico': icivico,
    });
    var thisurl = "/infoacquisto/";
    $.ajax({
      type: "POST",
      url: thisurl,
      data: { data: datainfo, data2: prodotto },
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: function (result) {
        window.console.log('Successful');
      }
    });
    binfo = true;

    sendInfo();
    return true;
    $('#submitBtn').click();

  }
  fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
      // Inizia Stripe.js
      const stripe = Stripe(data.publicKey);


      // Event handler
      try {
        document.querySelector("#submitBtn").addEventListener("click", () => {
          // Prendi il  Checkout Session ID
          fetch("/create-checkout-session/")
            .then((result) => { return result.json(); })
            .then((data) => {
              console.log(data);
              // Vai Stripe Checkout
              return stripe.redirectToCheckout({ sessionId: data.sessionId })
            })
            .then((res) => {
              console.log(res);
            });
        });
      }
      catch {
        return 0;
      }
    });
})
