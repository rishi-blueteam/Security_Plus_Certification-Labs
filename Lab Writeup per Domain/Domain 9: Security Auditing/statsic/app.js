const $ = (id) => document.getElementById(id);
const passwordInput = $("password");
const resultBox = $("result");
const emptyState = $("emptyState");
const listResults = $("listResults");

passwordInput.addEventListener("input", () => {
  $("charCount").textContent = `${passwordInput.value.length} characters`;
});

$("toggleVisibility").addEventListener("click", () => {
  const showing = passwordInput.type === "text";
  passwordInput.type = showing ? "password" : "text";
  $("toggleVisibility").textContent = showing ? "SHOW" : "HIDE";
});

function showError(message) {
  $("statusTag").textContent = "CHECK INPUT";
  emptyState.classList.remove("hidden");
  resultBox.classList.add("hidden");
  listResults.classList.add("hidden");
  emptyState.querySelector("h3").textContent = "Unable to analyze.";
  emptyState.querySelector("p").textContent = message;
}

function verdictClass(value, positiveWhenTrue = false) {
  if (value === "unavailable" || value === "not_checked") return "warn";
  return (value === true || value === "not_found" || value === "No") ? "good" : "bad";
}

function renderResult(r) {
  emptyState.classList.add("hidden");
  listResults.classList.add("hidden");
  resultBox.classList.remove("hidden");
  $("statusTag").textContent = "ANALYSIS COMPLETE";
  $("strength").textContent = r.strength;
  $("scoreChip").textContent = `${r.zxcvbn_score} / 4`;
  $("scoreBar").style.width = `${(r.zxcvbn_score / 4) * 100}%`;
  $("length").textContent = `${r.length} characters`;
  $("classes").textContent = `${r.class_count} of 4`;
  $("guesses").textContent = Number(r.guesses).toLocaleString();
  $("crackTime").textContent = r.crack_time_estimate;
  $("common").textContent = r.common_password ? "Yes" : "No";
  $("common").className = r.common_password ? "bad" : "good";
  $("repeated").textContent = r.repeated_characters ? "Detected" : "Not detected";
  $("repeated").className = r.repeated_characters ? "bad" : "good";
  $("sequences").textContent = r.predictable_sequences.length ? r.predictable_sequences.join(", ") : "Not detected";
  $("sequences").className = r.predictable_sequences.length ? "bad" : "good";
  const breachText = r.breach.status === "found"
    ? `Found · ${Number(r.breach.count).toLocaleString()} occurrences`
    : r.breach.status === "not_found" ? "Not found" :
      r.breach.status === "unavailable" ? "Check unavailable" : "Not checked";
  $("breach").textContent = breachText;
  $("breach").className = r.breach.status === "found" ? "bad" :
    r.breach.status === "not_found" ? "good" : "warn";
  $("recommendations").innerHTML = "";
  r.recommendations.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    $("recommendations").appendChild(li);
  });
  $("breachMessage").textContent = `${r.breach.message} Crack-time estimates are illustrative and depend on the attack model and hardware.`;
}

$("analyzeBtn").addEventListener("click", async () => {
  const password = passwordInput.value;
  if (!password) return showError("Enter a password first.");
  $("statusTag").textContent = "ANALYZING…";
  try {
    const response = await fetch("/api/analyze", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({password, check_breach: true})
    });
    const data = await response.json();
    if (!data.ok) return showError(data.error || "Analysis failed.");
    renderResult(data.result);
  } catch (_e) { showError("Could not reach the local Python service. Is the app running?"); }
});

$("clearBtn").addEventListener("click", () => {
  passwordInput.value = "";
  passwordInput.type = "password";
  $("toggleVisibility").textContent = "SHOW";
  $("charCount").textContent = "0 characters";
  resultBox.classList.add("hidden");
  listResults.classList.add("hidden");
  emptyState.classList.remove("hidden");
  emptyState.querySelector("h3").textContent = "Ready to inspect.";
  emptyState.querySelector("p").textContent = "Enter a password and run the analysis to view its security assessment.";
  $("statusTag").textContent = "AWAITING INPUT";
});

$("importBtn").addEventListener("click", async () => {
  const file = $("passwordFile").files[0];
  if (!file) return showError("Choose a .txt file first.");
  $("statusTag").textContent = "ANALYZING LIST…";
  const form = new FormData();
  form.append("file", file);
  try {
    const response = await fetch("/api/analyze-list", {method: "POST", body: form});
    const data = await response.json();
    if (!data.ok) return showError(data.error || "Import analysis failed.");
    emptyState.classList.add("hidden");
    resultBox.classList.add("hidden");
    listResults.classList.remove("hidden");
    $("statusTag").textContent = `${data.results.length} ENTRIES PROCESSED`;
    listResults.innerHTML = "";
    data.results.forEach((entry) => {
      const row = document.createElement("div");
      row.className = "list-row";
      const left = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = `Entry ${entry.index}`;
      const detail = document.createElement("small");
      detail.textContent = entry.error || `${entry.result.length} characters · zxcvbn ${entry.result.zxcvbn_score}/4 · breach: ${entry.result.breach.status}`;
      left.append(title, detail);
      const verdict = document.createElement("strong");
      verdict.textContent = entry.error ? "ERROR" : entry.result.strength.toUpperCase();
      verdict.className = entry.error ? "warn" : (entry.result.strength === "Strong" ? "good" : "warn");
      row.append(left, verdict);
      listResults.appendChild(row);
    });
    // Clear file input after processing; no password values are displayed.
    $("passwordFile").value = "";
  } catch (_e) { showError("Could not reach the local Python service. Is the app running?"); }
});
