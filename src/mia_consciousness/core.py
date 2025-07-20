import re
from typing import List, Dict

class CoreResearchAgent:
    """
    Agente principale per parsing e analisi delle risposte Ollama.
    Fornisce metodi per estrarre criticità, valutazioni, sintesi, applicazioni cliniche e roadmap da risposte testuali strutturate.
    """

    def _parse_critical_issues(self, response: str) -> List[Dict[str, str]]:
        """
        Estrae una lista di criticità dalla sezione LIMITATIONS o tramite fallback su parole chiave.
        Args:
            response (str): Testo della risposta Ollama.
        Returns:
            List[Dict[str, str]]: Lista di dizionari con titolo e descrizione della criticità.
        Raises:
            Nessuna eccezione specifica, ma input non stringa può causare errori.
        """
        issues = []
        # Cerca la sezione LIMITATIONS
        match = re.search(r"LIMITATIONS:\s*(.*?)(?:\n[A-Z_]+:|$)", response, re.DOTALL | re.IGNORECASE)
        if match:
            limitations_text = match.group(1).strip()
            # Suddivide in punti elenco o frasi
            points = re.split(r"(?:\n\s*[-*•]\s*|\n\d+\.\s*|\n)", limitations_text)
            for point in points:
                clean = point.strip("-•* ").strip()
                if clean:
                    # Prova a separare titolo e descrizione
                    if ':' in clean:
                        title, desc = clean.split(':', 1)
                        issues.append({"title": title.strip(), "description": desc.strip()})
                    else:
                        issues.append({"title": clean[:40], "description": clean})
        else:
            # Fallback: cerca frasi con parole chiave
            fallback = re.findall(r"([A-Z][^.!?]*?(?:limitation|bias|issue|problem|risk)[^.!?]*[.!?])", response, re.IGNORECASE)
            for sent in fallback:
                issues.append({"title": sent[:40], "description": sent.strip()})
        return issues

    def _extract_critical_assessment(self, response: str) -> str:
        """
        Estrae la valutazione critica complessiva dalla risposta.
        Args:
            response (str): Testo della risposta Ollama.
        Returns:
            str: Valutazione critica estratta o stringa vuota.
        """
        # Cerca una sezione dedicata
        match = re.search(r"CRITICAL_ASSESSMENT:\s*(.*?)(?:\n[A-Z_]+:|$)", response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # Fallback: cerca frasi con parole chiave
        fallback = re.findall(r"(Overall critical assessment:.*?)(?:\n|$)", response, re.IGNORECASE)
        if fallback:
            return fallback[0].strip()
        # Fallback: cerca frasi con parole come 'In summary', 'Critically', 'Overall'
        summary = re.findall(r"((?:In summary|Critically|Overall)[^\n\.]*[\n\.])", response, re.IGNORECASE)
        if summary:
            return summary[0].strip()
        # Se non trova nulla, restituisce stringa vuota
        return ""

    def _extract_synthesis_framework(self, response: str) -> str:
        """
        Estrae la sintesi/framework unificato dalla risposta.
        Args:
            response (str): Testo della risposta Ollama.
        Returns:
            str: Sintesi estratta o stringa vuota.
        """
        # Cerca una sezione dedicata
        match = re.search(r"SYNTHESIS_FRAMEWORK:\s*(.*?)(?:\n[A-Z_]+:|$)", response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # Fallback: cerca frasi con parole chiave
        fallback = re.findall(r"(Unified framework:.*?)(?:\n|$)", response, re.IGNORECASE)
        if fallback:
            return fallback[0].strip()
        # Fallback: cerca frasi con parole come 'In conclusion', 'Integrated', 'Synthesis'
        summary = re.findall(r"((?:In conclusion|Integrated|Synthesis)[^\n\.]*[\n\.])", response, re.IGNORECASE)
        if summary:
            return summary[0].strip()
        # Se non trova nulla, restituisce stringa vuota
        return ""

    def _extract_clinical_applications(self, response: str) -> List[str]:
        """
        Estrae una lista di applicazioni cliniche dalla risposta.
        Args:
            response (str): Testo della risposta Ollama.
        Returns:
            List[str]: Lista di applicazioni cliniche estratte.
        """
        applications = []
        # Cerca la sezione CLINICAL_APPLICATIONS
        match = re.search(r"CLINICAL_APPLICATIONS:\s*(.*?)(?:\n[A-Z_]+:|$)", response, re.DOTALL | re.IGNORECASE)
        if match:
            apps_text = match.group(1).strip()
            # Suddivide in punti elenco o frasi
            points = re.split(r"(?:\n\s*[-*•]\s*|\n\d+\.\s*|\n)", apps_text)
            for point in points:
                clean = point.strip("-•* ").strip()
                if clean:
                    applications.append(clean)
        else:
            # Fallback: cerca frasi con parole chiave
            fallback = re.findall(r"([A-Z][^.!?]*?(?:clinical application|therapy|diagnosis|treatment)[^.!?]*[.!?])", response, re.IGNORECASE)
            for sent in fallback:
                applications.append(sent.strip())
        return applications

    def _extract_research_roadmap(self, response: str) -> List[str]:
        """
        Estrae una lista di step futuri/roadmap dalla risposta.
        Args:
            response (str): Testo della risposta Ollama.
        Returns:
            List[str]: Lista di step/roadmap estratti.
        """
        roadmap = []
        # Cerca la sezione RESEARCH_ROADMAP
        match = re.search(r"RESEARCH_ROADMAP:\s*(.*?)(?:\n[A-Z_]+:|$)", response, re.DOTALL | re.IGNORECASE)
        if match:
            roadmap_text = match.group(1).strip()
            # Suddivide in punti elenco o frasi
            points = re.split(r"(?:\n\s*[-*•]\s*|\n\d+\.\s*|\n)", roadmap_text)
            for point in points:
                clean = point.strip("-•* ").strip()
                if clean:
                    roadmap.append(clean)
        else:
            # Fallback: cerca frasi con parole chiave
            fallback = re.findall(r"([A-Z][^.!?]*?(?:future work|next step|roadmap|research direction)[^.!?]*[.!?])", response, re.IGNORECASE)
            for sent in fallback:
                roadmap.append(sent.strip())
        return roadmap 