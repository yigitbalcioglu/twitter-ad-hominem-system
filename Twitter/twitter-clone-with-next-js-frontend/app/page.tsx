import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-[70vh] flex-col items-center justify-center px-6 text-center text-white">
      <div className="max-w-xl space-y-4">
        <h1 className="text-3xl font-bold sm:text-4xl">Welcome to Twitter Clone</h1>
        <p className="text-white/80">
          Login or create an account to see the timeline and start tweeting.
        </p>
        <div className="flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link
            href="/login"
            className="rounded-full bg-white px-6 py-2 text-sm font-semibold text-black transition hover:bg-white/90"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="rounded-full border border-white/50 px-6 py-2 text-sm font-semibold text-white transition hover:border-white"
          >
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}
