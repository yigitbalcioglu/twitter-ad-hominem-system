import React from 'react'
import RegisterForm from "../../../components/(auth)/RegisterForm"
import Link from "next/link"
import { signIn } from '@/lib/auth'

const page = () => {
    return (
        <main className="flex min-h-screen items-center justify-center bg-black px-6 py-10 text-white">
            <div className="grid w-full max-w-6xl gap-10 lg:grid-cols-2 lg:items-center">
                <section className="space-y-6">
                    <p className="text-5xl font-black leading-tight lg:text-7xl">X</p>
                    <h1 className="text-4xl font-extrabold leading-tight lg:text-6xl">Join today.</h1>
                    <p className="text-lg text-zinc-300">Kendi profilini olustur ve topluluga katil.</p>
                </section>

                <section className="w-full max-w-md rounded-3xl border border-zinc-800 bg-black p-8">
                    <h2 className="mb-2 text-3xl font-bold">Hesap olustur</h2>
                    <p className="mb-8 text-sm text-zinc-400">Dakikalar icinde kayit olabilirsin.</p>
                    <RegisterForm />

                    <form
                        className="mt-4"
                        action={async () => {
                            "use server";
                            await signIn("google");
                        }}
                    >
                        <button
                            type="submit"
                            className="w-full rounded-full border border-zinc-700 px-4 py-2 text-sm font-semibold text-white transition hover:border-zinc-500"
                        >
                            Google ile giris yap
                        </button>
                    </form>

                    <div className="mt-6 text-sm text-zinc-400">
                        Hesabin var mi?{" "}
                        <Link className="font-semibold text-sky-500 hover:underline" href="/login">
                            Giris yap
                        </Link>
                    </div>
                </section>
            </div>
        </main>
    );
};

export default page