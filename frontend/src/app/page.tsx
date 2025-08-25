"use client"

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  ArrowRight,
  PlayCircle,
  Brain,
  BookOpen,
  Rocket,
} from "lucide-react"
import { motion } from "framer-motion"

export default function LandingPage() {
  const { data: session } = useSession()
  const router = useRouter()

  const handleGetStarted = () => {
    if (session) {
      router.push("/dashboard")
    } else {
      router.push("/login")
    }
  }

  // floating animation variants
  const float = {
    animate: {
      y: [0, -20, 0],
      transition: {
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut",
      },
    },
  }

  return (
    <section className="relative flex flex-col items-center justify-center h-screen text-center bg-gradient-to-br from-blue-50 via-white to-teal-50 overflow-hidden px-6">
      {/* Floating background icons */}
      <motion.div
        className="absolute top-20 left-10 text-blue-400"
        variants={float}
        animate="animate"
      >
        <Brain size={64} />
      </motion.div>

      <motion.div
        className="absolute bottom-32 left-20 text-teal-400"
        variants={float}
        animate="animate"
        transition={{ delay: 1 }}
      >
        <BookOpen size={56} />
      </motion.div>

      <motion.div
        className="absolute top-32 right-16 text-indigo-400"
        variants={float}
        animate="animate"
        transition={{ delay: 0.5 }}
      >
        <Rocket size={60} />
      </motion.div>

      <motion.div
        className="absolute bottom-20 right-32 text-pink-400"
        variants={float}
        animate="animate"
        transition={{ delay: 1.2 }}
      >
        <Brain size={48} />
      </motion.div>

      {/* Extra scattered icons */}
      <motion.div
        className="absolute top-10 right-1/3 text-blue-300"
        variants={float}
        animate="animate"
        transition={{ delay: 0.8 }}
      >
        <BookOpen size={50} />
      </motion.div>

      <motion.div
        className="absolute bottom-10 left-1/3 text-teal-300"
        variants={float}
        animate="animate"
        transition={{ delay: 1.5 }}
      >
        <Rocket size={54} />
      </motion.div>

      <motion.div
        className="absolute top-1/2 left-1/4 text-indigo-300"
        variants={float}
        animate="animate"
        transition={{ delay: 0.6 }}
      >
        <Brain size={44} />
      </motion.div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 max-w-3xl"
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Badge
            variant="secondary"
            className="mb-4 px-4 py-1 rounded-full text-blue-700 bg-blue-100 shadow-sm"
          >
            AI-Powered Learning Platform
          </Badge>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-blue-500 to-teal-400 bg-clip-text text-transparent mb-4 leading-tight"
        >
          Learn Your Way
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-lg md:text-xl text-gray-700 mb-8"
        >
          Personalized education that adapts to your unique learning needs.
          <br />
          Built for accessibility, powered by AI.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.7 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Button
            onClick={handleGetStarted}
            className="px-6 py-3 text-lg rounded-xl bg-blue-600 hover:bg-blue-700 transition-all shadow-md hover:shadow-lg"
          >
            Get Started Free
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </motion.div>
      </motion.div>
    </section>
  )
}
