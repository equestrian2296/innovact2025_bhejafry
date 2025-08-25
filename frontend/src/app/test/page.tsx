"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Progress } from "@/components/ui/progress"
import { Label } from "@/components/ui/label"

type FlowchartStep = {
  step: string
  description: string
}

type MainNote = {
  heading: string
  points: string[]
}

type AnalysisResult = {
  flowchart: FlowchartStep[]
  tableOfContents: string[]
  mainNotes: MainNote[]
}

export default function TestAnalysePage() {
  const [inputText, setInputText] = useState("")
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyse = async () => {
    setLoading(true)
    setProgress(20)
    setResult(null)
    setError(null)

    try {
      const res = await fetch("/api/analyse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      })

      setProgress(60)

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        setError(err.error || "Unknown error")
        return
      }

      const data = await res.json()
      setResult(data)
      setProgress(100)
    } catch (err: any) {
      setError(err.message || "Request failed")
    } finally {
      setLoading(false)
      setTimeout(() => setProgress(0), 1500) // reset bar
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <Card className="max-w-4xl mx-auto shadow-lg border rounded-2xl">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">🔬 scRNA-seq Text Analysis</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Label htmlFor="input">Paste your text</Label>
          <Textarea
            id="input"
            placeholder="Paste your scRNA-seq text here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full"
            rows={6}
          />
          <Button onClick={handleAnalyse} disabled={loading || !inputText} className="w-full">
            {loading ? "Analysing..." : "Analyse"}
          </Button>

          {loading && (
            <Progress value={progress} className="h-2 rounded-full" />
          )}

          {error && <div className="text-red-600 mt-4">{error}</div>}

          {result && (
            <div className="mt-6 grid gap-6 md:grid-cols-2">
              {/* Flowchart */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">📊 Flowchart</CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-64 pr-4">
                    <ol className="list-decimal list-inside space-y-3">
                      {result.flowchart.map((step, i) => (
                        <li key={i} className="text-sm">
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger className="font-semibold cursor-help">
                                {step.step}
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>{step.description}</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </li>
                      ))}
                    </ol>
                  </ScrollArea>
                </CardContent>
              </Card>

              {/* Table of Contents */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">📖 Table of Contents</CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-64 pr-4">
                    <ul className="list-disc list-inside space-y-2 text-sm">
                      {result.tableOfContents.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  </ScrollArea>
                </CardContent>
              </Card>

              {/* Main Notes */}
              <Card className="md:col-span-2">
                <CardHeader>
                  <CardTitle className="text-lg">📝 Main Notes</CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-72 pr-4">
                    {result.mainNotes.map((note, i) => (
                      <div key={i} className="mb-6">
                        <h3 className="font-semibold text-base mb-2">{note.heading}</h3>
                        <ul className="list-disc list-inside ml-4 space-y-1 text-sm">
                          {note.points.map((point, j) => (
                            <li key={j}>{point}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
