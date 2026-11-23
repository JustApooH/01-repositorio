const STATUS_ORDER = ["todo", "in_progress", "done"];

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const details = body.details ? Object.values(body.details).join(" ") : "";
    throw new Error(details || body.error || "Erro inesperado");
  }
  return response;
}

function showError(message) {
  const box = document.getElementById("form-error");
  box.textContent = message;
  box.hidden = !message;
}

document.getElementById("task-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const payload = {
    title: form.title.value,
    description: form.description.value,
    priority: form.priority.value,
  };
  try {
    await request("/api/tasks", { method: "POST", body: JSON.stringify(payload) });
    window.location.reload();
  } catch (error) {
    showError(error.message);
  }
});

document.querySelector(".board").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const card = button.closest(".card");
  const id = card.dataset.id;
  const action = button.dataset.action;

  try {
    if (action === "delete") {
      if (!confirm("Excluir esta tarefa?")) return;
      await request(`/api/tasks/${id}`, { method: "DELETE" });
    } else if (action === "edit") {
      const title = prompt("Novo título:", card.querySelector("h3").textContent);
      if (title === null) return;
      await request(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({ title }),
      });
    } else {
      const current = STATUS_ORDER.indexOf(card.dataset.status);
      const next = current + (action === "forward" ? 1 : -1);
      if (next < 0 || next >= STATUS_ORDER.length) return;
      await request(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({ status: STATUS_ORDER[next] }),
      });
    }
    window.location.reload();
  } catch (error) {
    alert(error.message);
  }
});
