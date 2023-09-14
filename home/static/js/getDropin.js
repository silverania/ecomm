
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
    for (index = 0; index < inputs.length; ++index) {
      if (inputs[index].value != "") {
        continue;
      }
      else {
        alert("inserisci bene tutte le informazioni per la spedizione");
        return -1;
      }
    }
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
