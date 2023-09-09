
var button = document.querySelector('#submit-button');

function dropinCreate() {
  document.getElementById("submit-button").setAttribute("action", "/checkout");
  try {
    braintree.dropin.create({
      //authorization: "production_5r4mc5mt_wnz3hnyc64t2nhv9", container: "#dropin-container",
      //authorization: 'sandbox_kt24h5dd_tttvwsx23m9khfy6', container: "#dropin-container",
      authorization: client_token, container: "#dropin-container", locale: "it_IT",
    }, function (err, dropinInstance) {
      if (err) {
        // Handle any errors that might've occurred when creating Drop-in
        console.error(err);
        return;
      }
      document.getElementById("submit-button").addEventListener('click',
        function () {
          dropinInstance.requestPaymentMethod(function (err, payload) {
            /* il click sul button paga sul dropin button invia il
            pagamento cryptato in una variabile chiamata : payment method nonce*/
            $.ajax({
              type: 'POST',
              url: '/checkout',
              // esegue la view page in views.py
              headers: { 'X-CSRFToken': csrftoken }, /* riga necessaria solo su django,
questo token (csrftoken) non ha nulla a che vedere con il client_token per l 'autenticazione' su braintree , su framework diversi da django non serve*/
              data: { 'paymentMethodNonce': payload.nonce, 'amount': "" }
            }).done(function (result) {
              dropinInstance.teardown(function (teardownErr) {
                if (teardownErr) {
                  console.error('non posso resettare il dropin');
                } else {
                  console.info('dropin reset ok!');
                  $('#submit-button').remove(); $('#prezzo').remove();
                }
              });
              if (result.success) {
                $('#checkout-message').html('<h1>Success</h1><p>Your Drop-in UI is working! Check your <a href="https://sandbox.braintreegateway.com/login">sandbox Control Panel</a> for your test transactions.</p><p>Refresh to try another transaction.</p>');
              } else {
                console.log(result);
                $('#checkout-message').html('<h1>Error</h1><p>Check your console.</p>');
              }
            });
          });
        });
    });
  }

  catch (TypeError) {
    console.log(TypeError);
  }
}
