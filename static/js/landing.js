function calculer() {

  const employes = parseFloat(document.getElementById('nb-employes').value);
  const taches   = parseFloat(document.getElementById('nb-taches').value);
  const duree    = parseFloat(document.getElementById('duree-tache').value);

  if (!employes || !taches || !duree) {
    alert('Merci de remplir tous les champs 😊');
    return;
  }

  const minutesParJour    = employes * taches * duree * 0.30;
  const minutesParSemaine = minutesParJour * 5;
  const heures  = Math.floor(minutesParSemaine / 60);
  const minutes = Math.round(minutesParSemaine % 60);

  const resultDiv   = document.getElementById('calc-result');
  const resultValue = document.getElementById('result-value');

  if (heures > 0) {
    resultValue.textContent = `${heures}h${minutes > 0 ? minutes : ''} / semaine`;
  } else {
    resultValue.textContent = `${minutes} min / semaine`;
  }

  resultDiv.style.display = 'block';
  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

}
