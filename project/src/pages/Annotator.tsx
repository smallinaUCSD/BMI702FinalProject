import React, { useState, useEffect, useRef } from 'react';

interface DrugInfo {
  name: string;
  rxcui?: string;
  relatedInfo?: any;
  error?: string;
}

const Annotator = () => {
  const [patientNote, setPatientNote] = useState('');
  const [annotatedText, setAnnotatedText] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [debugInfo, setDebugInfo] = useState('');
  const [hoveredDrug, setHoveredDrug] = useState<DrugInfo | null>(null);
  const [isLoadingDrugInfo, setIsLoadingDrugInfo] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ top: 0, left: 0 });
  const tooltipRef = useRef<HTMLDivElement>(null);
  const annotatedResultRef = useRef<HTMLDivElement>(null);

  const fetchDrugInfo = async (drugName: string) => {
    setIsLoadingDrugInfo(true);
    try {
      const response = await fetch(
        `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=${encodeURIComponent(drugName.trim())}`
      );
      
      if (!response.ok) {
        throw new Error(`RxNorm API request failed with status ${response.status}`);
      }
      
      const data = await response.json();
      console.log("RxNorm API response:", data); 
      
      if (data.idGroup && data.idGroup.rxnormId && data.idGroup.rxnormId.length > 0) {
        const rxcui = data.idGroup.rxnormId[0];
        
        const infoResponse = await fetch(
          `https://rxnav.nlm.nih.gov/REST/rxcui/${rxcui}/allrelated.json`
        );
        
        if (!infoResponse.ok) {
          throw new Error(`RxNorm info request failed with status ${infoResponse.status}`);
        }
        
        const infoData = await infoResponse.json();
        console.log("RxNorm allrelated API response:", infoData); 
        
        setHoveredDrug({
          name: drugName,
          rxcui: rxcui,
          relatedInfo: infoData.allRelatedGroup?.conceptGroup || []
        });
      } else {
        setHoveredDrug({
          name: drugName,
          error: 'No RxNorm ID found for this drug'
        });
      }
    } catch (error) {
      console.error('Error fetching drug info:', error);
      setHoveredDrug({
        name: drugName,
        error: error instanceof Error ? error.message : 'Error loading drug information'
      });
    } finally {
      setIsLoadingDrugInfo(false);
    }
  };

  const processAnnotation = async () => {
    if (!apiKey) {
      setError('Please enter a Gemini API key');
      return;
    }

    setIsLoading(true);
    setError('');
    setDebugInfo('');
    
    try {
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      
      const prompt = `
        Analyze this medical note and identify:
        1. Drug names (wrap in <drug>drug name</drug>)
        2. Dosage information (wrap in <dosage>dosage info</dosage>)
        3. Route information (wrap in <route>route info</route>)
        4. Form information (wrap in <form>form info</form>)
        5. Dosage Measurement information (wrap in <measurement>dosage info</measurement>)
        
        Important:
        - Make sure to preserve the original text
        - Only annotate clear instances of drugs, dosages, route, form, dosage information
        - Return the COMPLETE original text with annotations inserted
        - Don't add any other text, explanations, or summaries
        
        Medical note: ${patientNote}
      `;

      const payload = {
        contents: [{
          parts: [{ text: prompt }]
        }]
      };

      const headers = {
        "Content-Type": "application/json"
      };

      setDebugInfo("Sending request to Gemini API...");
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}: ${await response.text()}`);
      }

      const data = await response.json();
      setDebugInfo(`Received response: ${JSON.stringify(data).substring(0, 100)}...`);
      
      const text = data.candidates[0].content.parts[0].text;
      
      const regex = /(<drug>.*?<\/drug>)|(<dosage>.*?<\/dosage>)|(<route>.*?<\/route>)|(<form>.*?<\/form>)|(<measurement>.*?<\/measurement>)|([^<]+)/g;
      const segments: string[] = [];
      let match;
      
      while ((match = regex.exec(text)) !== null) {
        if (match[0]) segments.push(match[0]);
      }
      
      if (segments.length === 0) {
        segments.push(text);
      }
      
      setAnnotatedText(segments);
    } catch (error) {
      console.error('Error processing annotation:', error);
      setError(`Error processing annotation: ${error instanceof Error ? error.message : String(error)}`);
      setDebugInfo(`Full error: ${JSON.stringify(error, Object.getOwnPropertyNames(error))}`);
    }
    
    setIsLoading(false);
  };

  const handleDrugHover = (e: React.MouseEvent, drugName: string) => {
    e.preventDefault();
    e.stopPropagation();
    
    const rect = e.currentTarget.getBoundingClientRect();
    const containerRect = annotatedResultRef.current?.getBoundingClientRect() || { top: 0, left: 0 };
    
    const viewportTop = rect.bottom + window.scrollY - containerRect.top + 5;
    const viewportLeft = rect.left + window.scrollX - containerRect.left;
    
    const containerWidth = containerRect.width;
    const tooltipWidth = 256; 
    
    let adjustedLeft = viewportLeft;
    if (viewportLeft + tooltipWidth > containerWidth) {
      adjustedLeft = Math.max(0, containerWidth - tooltipWidth);
    }
    
    setTooltipPosition({
      top: viewportTop,
      left: adjustedLeft
    });
    
    fetchDrugInfo(drugName);
  };

  const [closeTimeout, setCloseTimeout] = useState<NodeJS.Timeout | null>(null);
  
  const handleDrugLeave = () => {

    const timeout = setTimeout(() => {
      setHoveredDrug(null);
    }, 300); 
    
    setCloseTimeout(timeout);
  };

  const handleTooltipEnter = () => {
    if (closeTimeout) {
      clearTimeout(closeTimeout);
      setCloseTimeout(null);
    }
  };
  
  const handleTooltipLeave = () => {
    setHoveredDrug(null);
  };

  const getHighlightColor = (text: string) => {
    if (text.includes('<drug>')) return 'bg-blue-200';
    if (text.includes('<dosage>')) return 'bg-green-200';
    if (text.includes('<route>')) return 'bg-yellow-200';
    if (text.includes('<form>')) return 'bg-red-200';
    if (text.includes('<measurement>')) return 'bg-purple-200';
    return '';
  };

  const renderAnnotatedText = () => {
    return annotatedText.map((segment, index) => {
      const highlightColor = getHighlightColor(segment);
      const cleanText = segment.replace(/<\/?[^>]+(>|$)/g, '');
      
      if (segment.includes('<drug>')) {
        return (
          <span 
            key={index} 
            className={`${highlightColor} cursor-pointer inline-block rounded px-1`}
            onMouseEnter={(e) => handleDrugHover(e, cleanText)}
            onMouseLeave={handleDrugLeave}
          >
            {cleanText}
          </span>
        );
      }
      
      return (
        <span key={index} className={highlightColor ? `${highlightColor} inline-block rounded px-1` : ''}>
          {cleanText}
        </span>
      );
    });
  };

  const testAnnotation = () => {
    const sampleAnnotated = [
     "Patient is taking ",
    "<drug>Lisinopril</drug> ",
    "<dosage>10</dosage> ",
    "<measurement>mg</measurement> ",
    "<route>PO</route> ",
    "<form>tablet</form> ",
    "for hypertension. Also prescribed ",
    "<drug>Metformin</drug> ",
    "<dosage>500</dosage> ",
    "<measurement>mg</measurement> ",
    "<route>PO</route> ",
    "<form>tablet</form> ",
    "."
    ];
    setAnnotatedText(sampleAnnotated);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Medical Note Annotator</h1>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Gemini API Key
          </label>
          <input
            type="password"
            className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your Gemini API key"
          />
          <p className="text-xs text-gray-500 mt-1">
          </p>
        </div>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Patient Note
          </label>
          <textarea
            className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500"
            value={patientNote}
            onChange={(e) => setPatientNote(e.target.value)}
            placeholder="Enter the patient note here... (Example: Patient is taking Lisinopril 10mg twice daily for hypertension.)"
          />
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={processAnnotation}
            disabled={isLoading || !patientNote || !apiKey}
            className={`flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg ${
              isLoading || !patientNote || !apiKey ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
            } transition-colors`}
          >
            {isLoading ? 'Processing...' : 'Annotate Text'}
          </button>
          
          <button
            onClick={testAnnotation}
            className="px-4 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
            title="Test with sample data without using API"
          >
            Test
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            <div className="font-medium">Error:</div>
            <div>{error}</div>
            {debugInfo && (
              <details className="mt-2">
                <summary className="cursor-pointer text-sm">Debug info</summary>
                <pre className="text-xs mt-2 overflow-auto p-2 bg-red-50">{debugInfo}</pre>
              </details>
            )}
          </div>
        )}
        
        {annotatedText.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Annotated Result</h2>
            {}
            <div 
              ref={annotatedResultRef} 
              className="p-4 bg-gray-50 rounded-lg border relative min-h-24"
              style={{ position: 'relative' }}
            >
              {renderAnnotatedText()}
              
              {}
              {hoveredDrug && (
                <div 
                  ref={tooltipRef}
                  className="absolute z-10 bg-white border border-gray-200 rounded-md shadow-lg p-4 w-64"
                  style={{ 
                    top: `${tooltipPosition.top}px`, 
                    left: `${tooltipPosition.left}px`,
                    maxWidth: '90%',
                    pointerEvents: 'auto' 
                  }}
                  onMouseEnter={handleTooltipEnter}
                  onMouseLeave={handleTooltipLeave}
                >
                  {isLoadingDrugInfo ? (
                    <div className="flex items-center justify-center py-2">
                      <div className="w-5 h-5 border-t-2 border-blue-500 rounded-full animate-spin"></div>
                      <span className="ml-2">Loading drug info...</span>
                    </div>
                  ) : (
                    <>
                      <h3 className="font-bold text-lg border-b pb-2 mb-2">{hoveredDrug.name}</h3>
                      {hoveredDrug.error ? (
                        <div className="text-sm text-red-500">{hoveredDrug.error}</div>
                      ) : (
                        <>
                          {hoveredDrug.rxcui ? (
                            <>
                              <div className="text-sm mb-3">
                                <div className="font-medium mb-1">RxNorm ID:</div>
                                <div className="bg-gray-100 p-1 rounded">{hoveredDrug.rxcui}</div>
                              </div>
                              
                              <div className="mt-2 pt-2 border-t flex flex-col gap-2">
                                {}
                                <a 
                                  href={`https://mor.nlm.nih.gov/RxNav/search?searchBy=RXCUI&searchTerm=${hoveredDrug.rxcui}`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:bg-blue-50 p-1 rounded text-sm block font-medium"
                                  onClick={(e) => e.stopPropagation()}
                                >
                                  🔍 View in RxNav Browser
                                </a>
                                <a 
                                  href={`https://rxnav.nlm.nih.gov/REST/rxcui/${hoveredDrug.rxcui}/allrelated.json`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:bg-blue-50 p-1 rounded text-sm block"
                                  onClick={(e) => e.stopPropagation()}
                                >
                                  💻 View API Data
                                </a>
                              </div>
                            </>
                          ) : (
                            <div className="text-sm italic">No RxNorm ID found</div>
                          )}
                        </>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
            
            <div className="mt-4 flex flex-wrap gap-4">
              <div className="flex items-center">
                <div className="w-4 h-4 bg-blue-200 rounded mr-2"></div>
                <span className="text-sm">Drug Names (hover for RxNorm info)</span>
              </div>
              <div className="flex items-center">
                <div className="w-4 h-4 bg-green-200 rounded mr-2"></div>
                <span className="text-sm">Dosage</span>
              </div>
              <div className="flex items-center">
                <div className="w-4 h-4 bg-yellow-200 rounded mr-2"></div>
                <span className="text-sm">Route</span>
              </div>
              <div className="flex items-center">
                <div className="w-4 h-4 bg-red-200 rounded mr-2"></div>
                <span className="text-sm">Form</span>
              </div>
              <div className="flex items-center">
                <div className="w-4 h-4 bg-purple-200 rounded mr-2"></div>
                <span className="text-sm">Measurement</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Annotator;
