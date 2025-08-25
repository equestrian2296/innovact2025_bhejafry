"use client"

import { signIn, useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Brain, Book } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

export default function LoginPage() {
  const { data: session } = useSession()
  const router = useRouter()
  const [showAnimation, setShowAnimation] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 })

  const colors = [
    "text-pink-500",
    "text-blue-500",
    "text-green-500",
    "text-purple-500",
    "text-yellow-500",
    "text-red-500",
    "text-indigo-500",
  ]

  useEffect(() => {
    setMounted(true)
    setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    const handleResize = () =>
      setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  useEffect(() => {
    if (session) {
      setShowAnimation(true)
      setTimeout(() => {
        router.push("/dashboard")
      }, 6000) // let animation play before redirect
    }
  }, [session, router])

  return (
    <div className="relative flex items-center justify-center h-screen overflow-hidden bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100">
      {/* floating background objects */}
      {mounted &&
        Array.from({ length: 20 }).map((_, i) => {
          const color = colors[Math.floor(Math.random() * colors.length)]
          return (
            <motion.div
              key={i}
              className={`absolute ${color}`}
              initial={{
                x: Math.random() * windowSize.width - windowSize.width / 2,
                y: Math.random() * windowSize.height - windowSize.height / 2,
                opacity: 0,
                scale: 0.6,
              }}
              animate={{
                y: [null, (Math.random() - 0.5) * 80],
                x: [null, (Math.random() - 0.5) * 80],
                opacity: [0.4, 1, 0.4],
                scale: [0.8, 1.2, 0.8],
                rotate: 360,
              }}
              transition={{
                duration: 6 + Math.random() * 6,
                repeat: Infinity,
                repeatType: "mirror",
              }}
            >
              {i % 2 === 0 ? <Brain size={32} /> : <Book size={32} />}
            </motion.div>
          )
        })}

      {/* login card with glow */}
      <Card className="w-[350px] shadow-2xl rounded-2xl relative z-10 bg-white/80 backdrop-blur-md border border-white/40 animate-pulse-slow">
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-400 to-purple-400 blur-2xl opacity-40 animate-glow"></div>
        <CardHeader>
          <CardTitle className="text-center text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
            Welcome
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4 relative z-10">
          <Button
            onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
            className="w-full rounded-xl text-lg py-6 shadow-lg hover:scale-105 transition-all duration-300"
          >
            Sign in with Google
          </Button>
        </CardContent>
      </Card>

      {/* login success animation */}
      <AnimatePresence>
        {showAnimation && (
          <motion.div
            className="absolute inset-0 flex items-center justify-center bg-white z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="flex items-center gap-8"
              initial="hidden"
              animate="visible"
              variants={{
                hidden: {},
                visible: { transition: { staggerChildren: 0.3 } },
              }}
            >
              <motion.div
                initial={{ x: 300, rotate: 0, opacity: 0 }}
                animate={{ x: 0, rotate: 360, opacity: 1 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              >
                <Brain size={90} className="text-blue-600 drop-shadow-lg" />
              </motion.div>
              <motion.div
                initial={{ x: -300, rotate: 0, opacity: 0 }}
                animate={{ x: 0, rotate: -360, opacity: 1 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              >
                <Book size={90} className="text-green-600 drop-shadow-lg" />
              </motion.div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style jsx global>{`
        @keyframes glow {
          0%, 100% {
            opacity: 0.4;
            filter: blur(16px);
          }
          50% {
            opacity: 0.8;
            filter: blur(24px);
          }
        }
        .animate-glow {
          animation: glow 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}
