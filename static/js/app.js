document.getElementById("payBtn").addEventListener("click", async () => {
  try {
    const res = await fetch("/payments/pay/");
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url; // Redirige al checkout de Cryptomus
    } else {
      alert("Error al generar el pago");
      console.log(data);
    }
  } catch (err) {
    alert("Error de conexión con el backend");
    console.error(err);
  }
});