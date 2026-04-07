function calculer() {
  const employes = parseFloat(document.getElementById("nb-employes").value);
  const taches = parseFloat(document.getElementById("nb-taches").value);
  const duree = parseFloat(document.getElementById("duree-tache").value);

  if (!employes || !taches || !duree) {
    alert("Merci de remplir tous les champs");
    return;
  }

  const minutes_par_jour = employes * taches * duree * 0.3;
  const minutes_par_semaine = minutes_par_jour * 5;
  const heures = Math.floor(minutes_par_semaine / 60);
  const minutes = Math.round(minutes_par_semaine % 60);

  const result_div = document.getElementById("calc-result");
  const result_value = document.getElementById("result-value");

  if (heures > 0) {
    result_value.textContent = `${heures}h${minutes > 0 ? minutes : ""} / semaine`;
  } else {
    result_value.textContent = `${minutes} min / semaine`;
  }

  result_div.style.display = "block";
  result_div.scrollIntoView({ behavior: "smooth", block: "center" });
}
