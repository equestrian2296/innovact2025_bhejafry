"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"

export default function TestAnalysePage() {
  const [inputText, setInputText] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    flowchart: string[]
    tableOfContents: string[]
    mainNotes: string[]
  } | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyse = async () => {
    setLoading(true)
    setResult(null)
    setError(null)

    try {
      const res = await fetch("/api/analyse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        setError(err.error || "Unknown error")
        return
      }

      const data = await res.json()
      setResult(data)
    } catch (err: any) {
      setError(err.message || "Request failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Card className="max-w-3xl mx-auto shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl font-bold">scRNA-seq Text Analysis</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="Paste your scRNA-seq text here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full"
            rows={8}
          />
          <Button onClick={handleAnalyse} disabled={loading || !inputText}>
            {loading ? "Analysing..." : "Analyse"}
          </Button>

          {error && <div className="text-red-600 mt-4">{error}</div>}

          {result && (
            <div className="mt-6 space-y-6">
              <section>
                <h2 className="text-lg font-semibold mb-2">📊 Flowchart</h2>
                <ol className="list-decimal list-inside space-y-1">
                  {result.flowchart.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ol>
              </section>

              <section>
                <h2 className="text-lg font-semibold mb-2">📖 Table of Contents</h2>
                <ul className="list-disc list-inside space-y-1">
                  {result.tableOfContents.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h2 className="text-lg font-semibold mb-2">📝 Main Notes</h2>
                <ul className="list-disc list-inside space-y-1">
                  {result.mainNotes.map((note, i) => (
                    <li key={i}>{note}</li>
                  ))}
                </ul>
              </section>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
