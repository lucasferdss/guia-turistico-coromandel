(function () {

  const form =
    document.getElementById("contactForm") ||
    document.querySelector("form");

  if (!form) {
    console.warn("[contato] Formulário não encontrado.");
    return;
  }

  const $nome =
    document.getElementById("nome") ||
    form.querySelector('[name="nome"]');
  const $email =
    document.getElementById("email") ||
    form.querySelector('[name="email"]');
  const $mensagem =
    document.getElementById("mensagem") ||
    form.querySelector('[name="mensagem"]');

  const $btn = form.querySelector('button[type="submit"]');

  function isValidEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  async function enviarContato(e) {
    e.preventDefault();

    const nome = ($nome?.value || "").trim();
    const email = ($email?.value || "").trim();
    const mensagem = ($mensagem?.value || "").trim();

    if (!nome || !email || !mensagem) {
      alert("Preencha nome, e-mail e mensagem.");
      return;
    }
    if (!isValidEmail(email)) {
      alert("E-mail inválido.");
      $email?.focus();
      return;
    }

    try {
      $btn && ($btn.disabled = true);

      const resp = await fetch("/send-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email, mensagem }),
      });

      const data = await resp.json().catch(() => ({}));

      if (resp.ok && data?.success) {
        alert(data.message || "Contato enviado com sucesso!");
        form.reset();
      
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        alert(
          data?.message ||
            "Não foi possível enviar agora. Tente novamente mais tarde."
        );
      }
    } catch (err) {
      console.error(err);
      alert("Erro de rede ao enviar. Verifique sua conexão.");
    } finally {
      $btn && ($btn.disabled = false);
    }
  }

  form.addEventListener("submit", enviarContato);
})();
