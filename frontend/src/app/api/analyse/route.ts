import { NextResponse } from "next/server"

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const { text } = body

    if (!text) {
      return NextResponse.json({ error: "Missing text in request body" }, { status: 400 })
    }

    // Mock response (replace with Gemini API call later)
    const response = {
      flowchart: [
        "Step 1: Read text",
        "Step 2: Extract key info",
        "Step 3: Structure content",
      ],
      tableOfContents: [
        "Introduction",
        "Overview",
        "Protocols",
        "Applications",
      ],
      mainNotes: [
        "scRNA-seq studies single-cell gene expression",
        "Provides higher resolution than bulk RNA-seq",
        "Protocols: SMART-seq, Drop-seq, 10X Genomics",
        "Applications: cancer research, immunology, developmental biology",
      ],
    }

    return NextResponse.json(response)
  } catch (err) {
    return NextResponse.json({ error: "Invalid JSON or server error" }, { status: 500 })
  }
}

// Optional GET for testing in browser
export async function GET() {
  return NextResponse.json({ message: "API is working (GET test)" })
}
