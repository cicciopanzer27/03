from typing import Dict, Any

class OutputGenerator:
    """
    Generazione e formattazione degli output scientifici e clinici.
    Fornisce metodi per produrre sezioni di report, estrarre applicazioni cliniche, rischi, validazioni e conclusioni.
    """

    def _format_results_for_paper(self, results: Dict[str, Any]) -> str:
        """
        Formatta i risultati per un paper scientifico in markdown.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Testo markdown strutturato con abstract, metodi, risultati, discussione, conclusioni.
        """
        abstract = results.get('summary', {}).get('abstract', 'N/A')
        methods = results.get('protocol', {}).get('methodology', [])
        findings = results.get('domain_results', {})
        discussion = results.get('summary', {}).get('discussion', 'N/A')
        conclusion = results.get('summary', {}).get('conclusion', 'N/A')

        md = [
            '# Risultati della Ricerca',
            '## Abstract',
            abstract,
            '## Metodi',
            '\n'.join(f'- {m}' for m in methods) if methods else 'N/A',
            '## Risultati',
        ]
        # Sezioni per ogni dominio
        for domain, domain_data in findings.items():
            md.append(f'### {domain.capitalize()}')
            md.append(domain_data.get('findings', 'N/A'))
        md += [
            '## Discussione',
            discussion,
            '## Conclusioni',
            conclusion
        ]
        return '\n\n'.join(md)

    def _format_discussion_for_paper(self, results: Dict[str, Any]) -> str:
        """
        Formatta la discussione per un paper scientifico, includendo limiti e prospettive future.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Testo markdown della discussione.
        """
        discussion = results.get('summary', {}).get('discussion', '')
        limitations = results.get('summary', {}).get('limitations', '')
        future = results.get('summary', {}).get('future_directions', '')
        md = [
            '## Discussione',
            discussion or 'N/A',
            '### Limitazioni',
            limitations or 'N/A',
            '### Prospettive Future',
            future or 'N/A'
        ]
        return '\n\n'.join(md)

    def _format_limitations_for_paper(self, results: Dict[str, Any]) -> str:
        """
        Formatta la sezione limitazioni per un paper scientifico.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Testo markdown delle limitazioni.
        """
        limitations = results.get('summary', {}).get('limitations', '')
        if not limitations:
            # Prova a estrarre da domain_results
            domain_limits = []
            for domain, data in results.get('domain_results', {}).items():
                lim = data.get('limitations')
                if lim:
                    domain_limits.append(f"**{domain.capitalize()}**: {lim}")
            if domain_limits:
                limitations = '\n'.join(domain_limits)
            else:
                limitations = 'N/A'
        md = [
            '## Limitazioni',
            limitations
        ]
        return '\n\n'.join(md)

    def _extract_clinical_applications(self, results: Dict[str, Any], category: str) -> str:
        """
        Estrae e formatta le applicazioni cliniche per una categoria specifica.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
            category (str): Categoria di applicazione clinica ('immediate', 'future', ecc.).
        Returns:
            str: Elenco markdown delle applicazioni cliniche.
        """
        apps = []
        # Cerca nella sezione summary
        summary_apps = results.get('summary', {}).get('clinical_applications', {})
        if isinstance(summary_apps, dict):
            apps = summary_apps.get(category, [])
        elif isinstance(summary_apps, list) and category.lower() in ('all', 'tutte'):
            apps = summary_apps
        # Fallback: cerca nei domain_results
        if not apps:
            for domain, data in results.get('domain_results', {}).items():
                domain_apps = data.get('clinical_applications', {})
                if isinstance(domain_apps, dict):
                    apps += domain_apps.get(category, [])
                elif isinstance(domain_apps, list) and category.lower() in ('all', 'tutte'):
                    apps += domain_apps
        if not apps:
            return 'Nessuna applicazione clinica trovata.'
        return '\n'.join(f'- {a}' for a in apps)

    def _extract_immediate_clinical_applications(self, results: Dict[str, Any]) -> str:
        """
        Estrae e formatta le applicazioni cliniche immediate.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown delle applicazioni cliniche immediate.
        """
        return self._extract_clinical_applications(results, 'immediate')

    def _extract_future_clinical_applications(self, results: Dict[str, Any]) -> str:
        """
        Estrae e formatta le applicazioni cliniche future.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown delle applicazioni cliniche future.
        """
        return self._extract_clinical_applications(results, 'future')

    def _extract_validation_requirements(self, results: Dict[str, Any]) -> str:
        """
        Estrae i requisiti di validazione clinica.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown dei requisiti di validazione.
        """
        reqs = results.get('summary', {}).get('validation_requirements', '')
        if not reqs:
            for domain, data in results.get('domain_results', {}).items():
                dom_reqs = data.get('validation_requirements')
                if dom_reqs:
                    reqs += f"- {dom_reqs}\n"
        return reqs.strip() or 'Nessun requisito di validazione trovato.'

    def _extract_clinical_risks(self, results: Dict[str, Any]) -> str:
        """
        Estrae i rischi clinici.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown dei rischi clinici.
        """
        risks = results.get('summary', {}).get('clinical_risks', '')
        if not risks:
            for domain, data in results.get('domain_results', {}).items():
                dom_risks = data.get('clinical_risks')
                if dom_risks:
                    risks += f"- {dom_risks}\n"
        return risks.strip() or 'Nessun rischio clinico trovato.'

    def _extract_regulatory_considerations(self, results: Dict[str, Any]) -> str:
        """
        Estrae le considerazioni regolatorie.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown delle considerazioni regolatorie.
        """
        reg = results.get('summary', {}).get('regulatory_considerations', '')
        if not reg:
            for domain, data in results.get('domain_results', {}).items():
                dom_reg = data.get('regulatory_considerations')
                if dom_reg:
                    reg += f"- {dom_reg}\n"
        return reg.strip() or 'Nessuna considerazione regolatoria trovata.'

    def _extract_clinical_conclusions(self, results: Dict[str, Any]) -> str:
        """
        Estrae le conclusioni cliniche.
        Args:
            results (Dict[str, Any]): Dizionario con i risultati della ricerca.
        Returns:
            str: Elenco markdown delle conclusioni cliniche.
        """
        conc = results.get('summary', {}).get('clinical_conclusions', '')
        if not conc:
            for domain, data in results.get('domain_results', {}).items():
                dom_conc = data.get('clinical_conclusions')
                if dom_conc:
                    conc += f"- {dom_conc}\n"
        return conc.strip() or 'Nessuna conclusione clinica trovata.' 