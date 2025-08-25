import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const { text } = await req.json();
    if (!text) {
      return NextResponse.json({ error: "Missing text" }, { status: 400 });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    const modelId = "gemini-2.5-flash"; // Supported model
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${modelId}:generateContent?key=${apiKey}`;

    const geminiRes = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              {
                text: `
Transform the following biological text into a **valid JSON object** with this structure:

{
  "flowchart": ["step1", "step2", ...],
  "tableOfContents": ["heading1", "heading2", ...],
  "mainNotes": ["point1", "point2", ...]
}

Text:
${text}
`
              }
            ]
          }
        ],
        generationConfig: {
          response_mime_type: "application/json" // enforce JSON output
        }
      })
    });

    if (!geminiRes.ok) {
      const err = await geminiRes.json();
      return NextResponse.json(
        { error: `Gemini error: ${err.error?.message || err}` },
        { status: geminiRes.status }
      );
    }

    const data = await geminiRes.json();
    const rawText = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? "{}";

    // Always return valid JSON
    try {
      return NextResponse.json(JSON.parse(rawText));
    } catch {
      return NextResponse.json({ error: "Invalid JSON from Gemini", raw: rawText });
    }
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ message: "OK" });
}
