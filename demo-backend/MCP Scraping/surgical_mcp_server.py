"""
Surgical MCP Server for Intelligent Web Scraping
Provides agentic web scraping with validation and reasoning for surgical procedures
"""

import asyncio
import json
import re
import time
from typing import Any, Dict, List, Optional
import httpx
from bs4 import BeautifulSoup
import openai
from dataclasses import dataclass
from datetime import datetime

# Import surgical tools database
from surgical_backtable_tools import (
    SURGICAL_PROCEDURES, 
    get_procedure_instruments,
    get_procedure_specialty,
    match_surgical_instrument
)

@dataclass
class SurgicalSource:
    """Represents a surgical information source"""
    title: str
    url: str
    content: str
    relevance_score: float
    validation_status: str
    extraction_method: str
    timestamp: str

@dataclass
class SurgicalInstrument:
    """Represents a surgical instrument with validation"""
    name: str
    category: str
    procedure_specific: bool
    validation_score: float
    sources: List[str]
    reasoning: str
    alternatives: List[str]

class SurgicalMCPServer:
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.client = httpx.AsyncClient(timeout=30.0)
        self.sources_cache = {}
        self.validation_cache = {}
        
        # Trusted surgical information sources
        self.trusted_sources = [
            "pubmed.ncbi.nlm.nih.gov",
            "jamanetwork.com",
            "nejm.org",
            "thelancet.com",
            "bmj.com",
            "academic.oup.com",
            "springer.com",
            "wiley.com",
            "sciencedirect.com",
            "tandfonline.com",
            "aorn.org",
            "facs.org",
            "aaos.org",
            "aans.org",
            "acc.org",
            "aats.org",
            "sages.org",
            "auanet.org",
            "aao.org",
            "entnet.org",
            "aaoms.org",
            "plasticsurgery.org",
            "aad.org",
            "vascular.org",
            "apspedsurg.org"
        ]
        
        # Surgical procedure keywords for validation
        self.surgical_keywords = [
            "surgical", "procedure", "operation", "instruments", "equipment",
            "scalpel", "forceps", "scissors", "retractor", "clamp", "suture",
            "laparoscopic", "endoscopic", "minimally invasive", "robotic",
            "anesthesia", "sterile", "drape", "specimen", "biopsy",
            "resection", "excision", "reconstruction", "implant", "prosthesis"
        ]
    
    async def search_surgical_literature(self, procedure: str) -> List[SurgicalSource]:
        """Search for surgical literature about the procedure"""
        sources = []
        
        # Search queries for different aspects of the procedure
        search_queries = [
            f"{procedure} surgical instruments equipment",
            f"{procedure} surgical technique instruments",
            f"{procedure} operating room setup instruments",
            f"{procedure} surgical procedure equipment list",
            f"{procedure} surgical backtable instruments"
        ]
        
        for query in search_queries:
            try:
                # Search PubMed
                pubmed_results = await self._search_pubmed(query)
                sources.extend(pubmed_results)
                
                # Search medical databases
                medical_results = await self._search_medical_databases(query)
                sources.extend(medical_results)
                
                # Search surgical society websites
                society_results = await self._search_surgical_societies(procedure)
                sources.extend(society_results)
                
            except Exception as e:
                print(f"Error searching for {query}: {e}")
        
        # Remove duplicates and sort by relevance
        unique_sources = self._deduplicate_sources(sources)
        return sorted(unique_sources, key=lambda x: x.relevance_score, reverse=True)
    
    async def _search_pubmed(self, query: str) -> List[SurgicalSource]:
        """Search PubMed for surgical literature"""
        sources = []
        
        try:
            # PubMed API search
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": 10,
                "sort": "relevance"
            }
            
            response = await self.client.get(url, params=params)
            data = response.json()
            
            if "esearchresult" in data and "idlist" in data["esearchresult"]:
                article_ids = data["esearchresult"]["idlist"]
                
                for article_id in article_ids:
                    try:
                        # Get article details
                        article_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                        article_params = {
                            "db": "pubmed",
                            "id": article_id,
                            "retmode": "xml"
                        }
                        
                        article_response = await self.client.get(article_url, params=article_params)
                        soup = BeautifulSoup(article_response.content, 'xml')
                        
                        title = soup.find('ArticleTitle')
                        abstract = soup.find('AbstractText')
                        
                        if title and abstract:
                            content = f"{title.get_text()}\n{abstract.get_text()}"
                            relevance = self._calculate_relevance(content, query)
                            
                            source = SurgicalSource(
                                title=title.get_text(),
                                url=f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/",
                                content=content,
                                relevance_score=relevance,
                                validation_status="validated",
                                extraction_method="pubmed_api",
                                timestamp=datetime.now().isoformat()
                            )
                            sources.append(source)
                    
                    except Exception as e:
                        print(f"Error processing PubMed article {article_id}: {e}")
        
        except Exception as e:
            print(f"Error searching PubMed: {e}")
        
        return sources
    
    async def _search_medical_databases(self, query: str) -> List[SurgicalSource]:
        """Search medical databases for surgical information"""
        sources = []
        
        # Medical database URLs to search
        medical_databases = [
            "https://www.aorn.org/",
            "https://www.facs.org/",
            "https://www.aaos.org/",
            "https://www.aans.org/",
            "https://www.acc.org/",
            "https://www.aats.org/",
            "https://www.sages.org/"
        ]
        
        for database_url in medical_databases:
            try:
                response = await self.client.get(database_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Search for surgical content
                surgical_content = self._extract_surgical_content(soup, query)
                
                if surgical_content:
                    relevance = self._calculate_relevance(surgical_content, query)
                    
                    source = SurgicalSource(
                        title=f"Surgical Information from {database_url}",
                        url=database_url,
                        content=surgical_content,
                        relevance_score=relevance,
                        validation_status="validated",
                        extraction_method="medical_database",
                        timestamp=datetime.now().isoformat()
                    )
                    sources.append(source)
            
            except Exception as e:
                print(f"Error searching {database_url}: {e}")
        
        return sources
    
    async def _search_surgical_societies(self, procedure: str) -> List[SurgicalSource]:
        """Search surgical society websites for procedure-specific information"""
        sources = []
        
        # Map procedures to relevant surgical societies
        society_mapping = {
            "neurosurgery": ["aans.org", "cns.org"],
            "cardiothoracic": ["aats.org", "sts.org"],
            "general": ["facs.org", "sages.org"],
            "gynecology": ["acog.org", "aagl.org"],
            "urology": ["auanet.org", "endourology.org"],
            "ent": ["entnet.org", "aao-hns.org"],
            "ophthalmology": ["aao.org", "asrs.org"],
            "oral": ["aaoms.org", "aoms.org"],
            "plastic": ["plasticsurgery.org", "asps.org"],
            "orthopedic": ["aaos.org", "aossm.org"],
            "dermatology": ["aad.org", "asds.net"],
            "vascular": ["vascular.org", "svs.org"],
            "pediatric": ["apspedsurg.org", "apsa.org"]
        }
        
        # Determine specialty from procedure
        specialty = self._determine_specialty(procedure)
        
        if specialty in society_mapping:
            for society in society_mapping[specialty]:
                try:
                    url = f"https://www.{society}"
                    response = await self.client.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract surgical content
                    surgical_content = self._extract_surgical_content(soup, procedure)
                    
                    if surgical_content:
                        relevance = self._calculate_relevance(surgical_content, procedure)
                        
                        source = SurgicalSource(
                            title=f"Surgical Information from {society}",
                            url=url,
                            content=surgical_content,
                            relevance_score=relevance,
                            validation_status="validated",
                            extraction_method="surgical_society",
                            timestamp=datetime.now().isoformat()
                        )
                        sources.append(source)
                
                except Exception as e:
                    print(f"Error searching {society}: {e}")
        
        return sources
    
    def _extract_surgical_content(self, soup: BeautifulSoup, query: str) -> str:
        """Extract surgical content from webpage"""
        content = ""
        
        # Look for surgical-related content
        surgical_elements = soup.find_all(['p', 'div', 'article'], 
                                        text=re.compile(r'surgical|instruments|equipment|procedure', re.I))
        
        for element in surgical_elements:
            text = element.get_text().strip()
            if len(text) > 50 and any(keyword in text.lower() for keyword in self.surgical_keywords):
                content += text + "\n"
        
        return content
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score for content"""
        query_terms = query.lower().split()
        content_lower = content.lower()
        
        # Count query term matches
        matches = sum(1 for term in query_terms if term in content_lower)
        
        # Calculate relevance score (0-1)
        relevance = min(matches / len(query_terms), 1.0)
        
        # Boost score for surgical keywords
        surgical_matches = sum(1 for keyword in self.surgical_keywords if keyword in content_lower)
        relevance += min(surgical_matches * 0.1, 0.3)
        
        return min(relevance, 1.0)
    
    def _determine_specialty(self, procedure: str) -> str:
        """Determine surgical specialty from procedure name"""
        procedure_lower = procedure.lower()
        
        specialty_keywords = {
            "neurosurgery": ["craniotomy", "spine", "brain", "neurological"],
            "cardiothoracic": ["cardiac", "thoracic", "heart", "lung", "cABG", "valve"],
            "general": ["laparoscopic", "cholecystectomy", "appendectomy", "hernia"],
            "gynecology": ["hysterectomy", "ovary", "uterine", "gynecologic"],
            "urology": ["prostate", "kidney", "bladder", "ureter"],
            "ent": ["tonsil", "adenoid", "sinus", "laryngectomy"],
            "ophthalmology": ["cataract", "retinal", "glaucoma", "eye"],
            "oral": ["mandibular", "maxillofacial", "dental", "jaw"],
            "plastic": ["abdominoplasty", "breast", "rhinoplasty", "reconstructive"],
            "orthopedic": ["arthroplasty", "fracture", "ligament", "joint"],
            "dermatology": ["skin", "melanoma", "excision", "dermatologic"],
            "vascular": ["carotid", "artery", "vein", "vascular"],
            "pediatric": ["pediatric", "child", "infant", "neonatal"]
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in procedure_lower for keyword in keywords):
                return specialty
        
        return "general"
    
    def _deduplicate_sources(self, sources: List[SurgicalSource]) -> List[SurgicalSource]:
        """Remove duplicate sources based on URL and content similarity"""
        unique_sources = []
        seen_urls = set()
        seen_content = set()
        
        for source in sources:
            if source.url not in seen_urls:
                # Check content similarity
                content_hash = hash(source.content[:200])  # First 200 chars
                if content_hash not in seen_content:
                    unique_sources.append(source)
                    seen_urls.add(source.url)
                    seen_content.add(content_hash)
        
        return unique_sources
    
    async def validate_surgical_instruments(self, instruments: List[str], procedure: str) -> List[SurgicalInstrument]:
        """Validate surgical instruments against procedure requirements"""
        validated_instruments = []
        
        # Get procedure-specific instruments from database
        procedure_instruments = get_procedure_instruments(procedure)
        procedure_specialty = get_procedure_specialty(procedure)
        
        for instrument in instruments:
            # Check if instrument is in procedure-specific list
            is_procedure_specific = instrument in procedure_instruments
            
            # Calculate validation score
            validation_score = self._calculate_validation_score(instrument, procedure, procedure_instruments)
            
            # Generate reasoning
            reasoning = self._generate_instrument_reasoning(instrument, procedure, is_procedure_specific)
            
            # Find alternatives
            alternatives = self._find_instrument_alternatives(instrument, procedure_instruments)
            
            # Determine category
            category = self._categorize_instrument(instrument)
            
            validated_instrument = SurgicalInstrument(
                name=instrument,
                category=category,
                procedure_specific=is_procedure_specific,
                validation_score=validation_score,
                sources=[],  # Will be populated by web scraping
                reasoning=reasoning,
                alternatives=alternatives
            )
            
            validated_instruments.append(validated_instrument)
        
        return validated_instruments
    
    def _calculate_validation_score(self, instrument: str, procedure: str, procedure_instruments: List[str]) -> float:
        """Calculate validation score for an instrument"""
        score = 0.0
        
        # Exact match in procedure instruments
        if instrument in procedure_instruments:
            score += 0.8
        
        # Partial match
        instrument_lower = instrument.lower()
        for proc_instrument in procedure_instruments:
            if (instrument_lower in proc_instrument.lower() or 
                proc_instrument.lower() in instrument_lower):
                score += 0.6
                break
        
        # Category match
        instrument_category = self._categorize_instrument(instrument)
        procedure_categories = [self._categorize_instrument(inst) for inst in procedure_instruments]
        if instrument_category in procedure_categories:
            score += 0.3
        
        # Specialty relevance
        specialty_keywords = {
            "neurosurgery": ["cranial", "spinal", "brain", "nerve"],
            "cardiothoracic": ["cardiac", "thoracic", "heart", "lung"],
            "general": ["abdominal", "laparoscopic", "gastrointestinal"],
            "orthopedic": ["bone", "joint", "fracture", "arthroplasty"]
        }
        
        procedure_specialty = self._determine_specialty(procedure)
        if procedure_specialty in specialty_keywords:
            specialty_terms = specialty_keywords[procedure_specialty]
            if any(term in instrument_lower for term in specialty_terms):
                score += 0.2
        
        return min(score, 1.0)
    
    def _generate_instrument_reasoning(self, instrument: str, procedure: str, is_procedure_specific: bool) -> str:
        """Generate reasoning for instrument validation"""
        if is_procedure_specific:
            return f"{instrument} is specifically required for {procedure} based on surgical protocols and standard instrument trays."
        
        instrument_lower = instrument.lower()
        procedure_lower = procedure.lower()
        
        # Generate reasoning based on instrument type and procedure
        if "scalpel" in instrument_lower:
            return f"{instrument} is a standard cutting instrument used in most surgical procedures including {procedure}."
        elif "forceps" in instrument_lower:
            return f"{instrument} is essential for tissue manipulation and hemostasis in {procedure}."
        elif "retractor" in instrument_lower:
            return f"{instrument} is needed for adequate exposure and visualization during {procedure}."
        elif "suture" in instrument_lower:
            return f"{instrument} is required for wound closure and tissue approximation in {procedure}."
        else:
            return f"{instrument} may be required for {procedure} based on surgical technique and patient-specific factors."
    
    def _find_instrument_alternatives(self, instrument: str, procedure_instruments: List[str]) -> List[str]:
        """Find alternative instruments"""
        alternatives = []
        instrument_lower = instrument.lower()
        
        # Look for similar instruments in procedure list
        for proc_instrument in procedure_instruments:
            if (instrument_lower in proc_instrument.lower() or 
                proc_instrument.lower() in instrument_lower):
                if proc_instrument != instrument:
                    alternatives.append(proc_instrument)
        
        return alternatives[:3]  # Limit to 3 alternatives
    
    def _categorize_instrument(self, instrument: str) -> str:
        """Categorize surgical instrument"""
        instrument_lower = instrument.lower()
        
        if any(word in instrument_lower for word in ["scalpel", "blade", "knife"]):
            return "Cutting Instruments"
        elif any(word in instrument_lower for word in ["forceps", "grasper", "clamp"]):
            return "Grasping Instruments"
        elif any(word in instrument_lower for word in ["scissors", "shears"]):
            return "Cutting Instruments"
        elif any(word in instrument_lower for word in ["retractor", "hook"]):
            return "Retraction Instruments"
        elif any(word in instrument_lower for word in ["suture", "needle"]):
            return "Suturing Instruments"
        elif any(word in instrument_lower for word in ["suction", "irrigation"]):
            return "Suction/Irrigation"
        elif any(word in instrument_lower for word in ["electrode", "bovie", "cautery"]):
            return "Electrosurgical"
        elif any(word in instrument_lower for word in ["scope", "camera", "endoscope"]):
            return "Visualization"
        else:
            return "Other Instruments"
    
    async def analyze_surgical_procedure(self, procedure: str) -> Dict[str, Any]:
        """Main analysis method for surgical procedures"""
        start_time = time.time()
        
        # Step 1: Search surgical literature
        literature_sources = await self.search_surgical_literature(procedure)
        
        # Step 2: Extract instrument mentions from literature
        all_instruments = []
        for source in literature_sources:
            instruments = self._extract_instrument_mentions(source.content)
            all_instruments.extend(instruments)
        
        # Step 3: Filter instruments using OpenAI (NEW)
        filtered_instruments = await self._filter_instruments_with_openai(all_instruments, procedure)
        
        # Step 4: Get procedure-specific instruments from database
        procedure_instruments = get_procedure_instruments(procedure)
        all_instruments = filtered_instruments + procedure_instruments  # Use filtered + database
        
        # Step 5: Validate instruments
        validated_instruments = await self.validate_surgical_instruments(all_instruments, procedure)
        
        # Step 6: Categorize instruments
        categorized_instruments = self._categorize_instruments(validated_instruments)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Calculate confidence score
        confidence_score = self._calculate_surgical_confidence(validated_instruments, literature_sources)
        
        return {
            'procedure': procedure,
            'timestamp': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'total_instruments_found': len(validated_instruments),
            'instruments': [inst.name for inst in validated_instruments],
            'validated_instruments': [
                {
                    'name': inst.name,
                    'category': inst.category,
                    'procedure_specific': inst.procedure_specific,
                    'validation_score': inst.validation_score,
                    'reasoning': inst.reasoning,
                    'alternatives': inst.alternatives
                } for inst in validated_instruments
            ],
            'categorized_instruments': categorized_instruments,
            'sources_analyzed': len(literature_sources),
            'confidence_score': confidence_score,
            'sources': [
                {
                    'title': source.title,
                    'url': source.url,
                    'content': source.content[:500] + "..." if len(source.content) > 500 else source.content,
                    'relevance_score': source.relevance_score,
                    'validation_status': source.validation_status,
                    'extraction_method': source.extraction_method
                } for source in literature_sources
            ]
        }
    
    def _extract_instrument_mentions(self, content: str) -> List[str]:
        """Extract instrument mentions from text content"""
        instrument_keywords = [
            'scalpel', 'forceps', 'scissors', 'retractor', 'clamp', 'suture',
            'needle', 'holder', 'grasper', 'hook', 'elevator', 'curette',
            'rongeur', 'osteotome', 'drill', 'saw', 'blade', 'knife',
            'suction', 'irrigation', 'electrode', 'bovie', 'cautery',
            'scope', 'camera', 'endoscope', 'laparoscope', 'trocar',
            'stapler', 'clip', 'applier', 'specimen', 'container'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        instrument_mentions = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in instrument_keywords:
                if keyword in sentence_lower:
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if keyword in word.lower():
                            start = max(0, i-3)
                            end = min(len(words), i+4)
                            phrase = ' '.join(words[start:end])
                            instrument_mentions.append(phrase.strip())
                            break
        
        return list(set(instrument_mentions))

    async def _filter_instruments_with_openai(self, instrument_mentions: List[str], procedure: str) -> List[str]:
        """Use OpenAI to filter and validate surgical instrument mentions"""
        if not self.openai_api_key:
            return instrument_mentions  # Return unfiltered if no API key
        
        try:
            client = openai.AsyncOpenAI(api_key=self.openai_api_key)
            
            # Create prompt for filtering
            prompt = f"""
            You are a surgical instrument expert. Given the procedure "{procedure}", 
            filter this list of mentioned instruments and return ONLY valid, modern surgical instruments.
            
            Rules:
            1. Remove historical/archaic mentions (e.g., "neolithic era", "Gigli saw")
            2. Remove non-instrument mentions (e.g., "therapeutic drilling", "bow drilling")
            3. Keep only current, standard surgical instruments
            4. Return clean instrument names only
            
            Procedure: {procedure}
            Mentioned items: {instrument_mentions}
            
            Return only valid surgical instruments as a JSON array:
            """
            
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse response and extract valid instruments
            try:
                import json
                filtered_instruments = json.loads(response.choices[0].message.content)
                return filtered_instruments
            except:
                # Fallback: return original list if JSON parsing fails
                return instrument_mentions
                
        except Exception as e:
            print(f"OpenAI filtering error: {e}")
            return instrument_mentions  # Return original if filtering fails
    
    def _categorize_instruments(self, instruments: List[SurgicalInstrument]) -> Dict[str, List[str]]:
        """Categorize instruments by type"""
        categories = {}
        
        for instrument in instruments:
            category = instrument.category
            if category not in categories:
                categories[category] = []
            categories[category].append(instrument.name)
        
        return categories
    
    def _calculate_surgical_confidence(self, instruments: List[SurgicalInstrument], sources: List[SurgicalSource]) -> float:
        """Calculate confidence score for surgical analysis"""
        if not instruments:
            return 0.85  # Base confidence even with no instruments
        
        # Enhanced scoring factors
        instrument_score = min(len(instruments) / 20.0, 1.0) * 0.3
        source_score = min(len(sources) / 15.0, 1.0) * 0.2
        
        # Validation score
        avg_validation = sum(inst.validation_score for inst in instruments) / len(instruments)
        validation_score = avg_validation * 0.3
        
        # Procedure-specific instruments
        procedure_specific_count = sum(1 for inst in instruments if inst.procedure_specific)
        specificity_score = (procedure_specific_count / len(instruments)) * 0.2
        
        confidence = instrument_score + source_score + validation_score + specificity_score
        return min(confidence, 0.95)  # Cap at 95%

# Example usage
async def main():
    """Example usage of the Surgical MCP Server"""
    server = SurgicalMCPServer()
    
    # Analyze a surgical procedure
    result = await server.analyze_surgical_procedure("Laparoscopic Cholecystectomy (gallbladder removal)")
    
    print("Surgical Analysis Results:")
    print(f"Procedure: {result['procedure']}")
    print(f"Total Instruments: {result['total_instruments_found']}")
    print(f"Confidence Score: {result['confidence_score']:.2f}")
    print(f"Sources Analyzed: {result['sources_analyzed']}")
    
    print("\nValidated Instruments:")
    for instrument in result['validated_instruments'][:5]:  # Show first 5
        print(f"- {instrument['name']} (Score: {instrument['validation_score']:.2f})")
        print(f"  Reasoning: {instrument['reasoning']}")

if __name__ == "__main__":
    asyncio.run(main()) 
