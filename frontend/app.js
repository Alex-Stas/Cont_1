async function requestJson(path) {
  const response = await fetch(`/api${path}`);
  let data = null;

  try {
    data = await response.json();
  } catch (error) {
    data = { error: "Invalid JSON response" };
  }

  if (!response.ok) {
    const message = data && data.error ? data.error : "Request failed";
    throw new Error(message);
  }

  return data;
}

function setPrettyJson(elementId, payload) {
  const element = document.getElementById(elementId);
  element.textContent = JSON.stringify(payload, null, 2);
}

function setError(elementId, error) {
  const element = document.getElementById(elementId);
  element.textContent = `Error: ${error.message}`;
}

document.getElementById("btn-health").addEventListener("click", async () => {
  try {
    const data = await requestJson("/health");
    setPrettyJson("system-output", { endpoint: "/health", data });
  } catch (error) {
    setError("system-output", error);
  }
});

document.getElementById("btn-info").addEventListener("click", async () => {
  try {
    const data = await requestJson("/info");
    setPrettyJson("system-output", { endpoint: "/info", data });
  } catch (error) {
    setError("system-output", error);
  }
});

document.getElementById("percent-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const a = document.getElementById("percent-a").value.trim();
  const b = document.getElementById("percent-b").value.trim();

  try {
    const data = await requestJson(`/percent/${encodeURIComponent(a)}/${encodeURIComponent(b)}`);
    setPrettyJson("percent-output", data);
  } catch (error) {
    setError("percent-output", error);
  }
});

document.getElementById("factorial-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const x = document.getElementById("factorial-x").value.trim();

  try {
    const data = await requestJson(`/fact/${encodeURIComponent(x)}`);
    setPrettyJson("factorial-output", data);
  } catch (error) {
    setError("factorial-output", error);
  }
});
