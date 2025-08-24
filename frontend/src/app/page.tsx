"use client"

import { signIn, signOut, useSession } from "next-auth/react"

export default function Home() {
  const { data: session } = useSession()

  return (
    <main className="flex flex-col items-center justify-center h-screen">
      {session ? (
        <>
          <p>Signed in as {session.user?.email}</p>
          <button onClick={() => signOut()}>Sign out</button>
        </>
      ) : (
        <button onClick={() => signIn("google")}>Sign in with Google</button>
      )}
    </main>
  )
}
