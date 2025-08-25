"use client"

import { useSession, signOut } from "next-auth/react"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Upload } from "lucide-react"

export default function Dashboard() {
  const { data: session } = useSession()
  const router = useRouter()
  const [theme, setTheme] = useState("Dyslexia Support")
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  // Load saved preference from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("learningTheme")
    if (saved) setTheme(saved)
  }, [])

  // Save preference to localStorage
  const handleThemeChange = (value: string) => {
    setTheme(value)
    localStorage.setItem("learningTheme", value)
  }

  // Upload file to API
  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    const formData = new FormData()
    formData.append("file", file)

    await fetch("/api/upload", {
      method: "POST",
      body: formData,
    })

    setUploading(false)
    setFile(null)
    alert("File uploaded successfully ✅")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navbar */}
      <nav className="flex justify-between items-center p-6 bg-white shadow-md">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-700">{session?.user?.name}</span>
          <Button 
            variant="destructive" 
            onClick={() => signOut({ callbackUrl: "/" })}
          >
            Logout
          </Button>
        </div>
      </nav>

      <div className="p-8 space-y-8">
        {/* Welcome Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <h2 className="text-2xl font-bold">
            Hi {session?.user?.name}, Ready to learn your way?
          </h2>
          <p className="text-gray-500">Let’s continue your learning journey today.</p>
        </div>

        {/* Profile + Preferences */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="rounded-2xl shadow-md">
            <CardHeader>
              <CardTitle>Learner Profile</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p><strong>Name:</strong> {session?.user?.name}</p>
              <p><strong>Email:</strong> {session?.user?.email}</p>

              {/* Theme selector */}
              <div>
                <p className="font-semibold mb-1">Learning Preference</p>
                <Select value={theme} onValueChange={handleThemeChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select theme" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Dyslexia Support">Dyslexia Support</SelectItem>
                    <SelectItem value="Dysgraphia Support">Dysgraphia Support</SelectItem>
                    <SelectItem value="ADHD Support">ADHD Support</SelectItem>
                    <SelectItem value="Visual Processing Disorder">
                      Visual Processing Disorder
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button 
                className="w-full mt-2 rounded-xl"
                onClick={() => router.push("/learn")}
              >
                Start Learning
              </Button>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="rounded-2xl shadow-md">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="flex gap-4">
              {/* Upload File */}
              <Dialog>
                <DialogTrigger asChild>
                  <Button className="flex items-center gap-2 rounded-xl">
                    <Upload size={18} /> Upload Textbook/PDF
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Upload File</DialogTitle>
                  </DialogHeader>
                  <input
                    type="file"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="my-4"
                  />
                  <Button 
                    onClick={handleUpload} 
                    disabled={!file || uploading}
                    className="w-full"
                  >
                    {uploading ? "Uploading..." : "Upload"}
                  </Button>
                </DialogContent>
              </Dialog>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
