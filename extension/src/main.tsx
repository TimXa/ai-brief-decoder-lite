import React from "react";
import ReactDOM from "react-dom/client";
import "./style.css";

type Risk = {
  risk: string;
  severity: "low" | "medium" | "high";
  reason: string;
};

type DecodedBrief = {
  summary: string;
  goals: string[];
  deliverables: string[];
  constraints: string[];
  risks: Risk[];
  clarifying_questions: string[];
  recommended_next_action: string;
};

type DecodeResponse = {
  run_id: string;
  status: "completed" | "failed";
  result: DecodedBrief | null;
  error: { code: string; message: string } | null;
};

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const sampleBrief = `We need a landing page for a B2B SaaS analytics product.
The page should explain the product, include pricing teaser,
capture emails, and be ready in 2 weeks.
Budget is limited. We also need copy suggestions and basic SEO.`;

function Section({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return (
    <section>
      <h2>{title}</h2>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function App() {
  const [text, setText] = React.useState(sampleBrief);
  const [response, setResponse] = React.useState<DecodeResponse | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [copied, setCopied] = React.useState(false);

  async function decodeBrief() {
    setLoading(true);
    setError(null);
    setCopied(false);
    try {
      const res = await fetch(`${API_URL}/v1/briefs/decode`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      if (!res.ok) {
        throw new Error(`Request failed with ${res.status}`);
      }
      setResponse(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  async function copyResult() {
    if (!response?.result) return;
    await navigator.clipboard.writeText(JSON.stringify(response.result, null, 2));
    setCopied(true);
  }

  const result = response?.result;

  return (
    <main>
      <header>
        <p className="eyebrow">AI Brief Decoder Lite</p>
        <h1>Decode a client brief</h1>
      </header>

      <div className="workspace">
        <div className="composer">
          <label htmlFor="brief">Brief text</label>
          <textarea id="brief" value={text} onChange={(event) => setText(event.target.value)} />

          <div className="actions">
            <button onClick={decodeBrief} disabled={loading || text.trim().length < 20}>
              {loading ? "Decoding..." : "Run decoder"}
            </button>
            <button className="secondary" onClick={copyResult} disabled={!result}>
              {copied ? "Copied" : "Copy JSON"}
            </button>
          </div>

          {error && <div className="error">{error}</div>}
          {response?.error && (
            <div className="error">
              {response.error.code}: {response.error.message}
            </div>
          )}
        </div>

        {result ? (
          <div className="result">
            <section>
              <h2>Summary</h2>
              <p>{result.summary}</p>
            </section>
            <Section title="Goals" items={result.goals} />
            <Section title="Deliverables" items={result.deliverables} />
            <Section title="Constraints" items={result.constraints} />
            <section>
              <h2>Risks</h2>
              {result.risks.map((risk) => (
                <article className="risk" key={risk.risk}>
                  <strong>{risk.severity}</strong>
                  <p>{risk.risk}</p>
                  <span>{risk.reason}</span>
                </article>
              ))}
            </section>
            <Section title="Questions" items={result.clarifying_questions} />
            <section>
              <h2>Next action</h2>
              <p>{result.recommended_next_action}</p>
            </section>
          </div>
        ) : (
          <div className="empty">
            Run the decoder to get a normalized summary, goals, deliverables, risks, questions and next action.
          </div>
        )}
      </div>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
