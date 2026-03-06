import React from 'react'
import LoginForm from "../../../components/(auth)/LoginForm"
import Link from "next/link"
import { FC } from "react"

interface ILoginPageProps {
    searchParams: {
        redirect?: string
    }
}


const LoginPage: FC<ILoginPageProps> = ({ searchParams }) => {
    return (
        <main className="flex min-h-screen items-center justify-center bg-black px-6 py-10 text-white">
            <div className="grid w-full max-w-6xl gap-10 lg:grid-cols-2 lg:items-center">
                <section className="space-y-6">
                    <p className="text-5xl font-black leading-tight lg:text-7xl">X</p>
                    <h1 className="text-4xl font-extrabold leading-tight lg:text-6xl">Happening now</h1>
                    <p className="text-lg text-zinc-300">Paylas, yorum yap, topluluguna baglan.</p>
                </section>

                <section className="w-full max-w-md rounded-3xl border border-zinc-800 bg-black p-8">
                    <h2 className="mb-2 text-3xl font-bold">Giris yap</h2>
                    <p className="mb-8 text-sm text-zinc-400">Hesabina devam etmek icin bilgilerini gir.</p>
                    <LoginForm />
                    <div className="mt-6 text-sm text-zinc-400">
                        Hesabin yok mu?{" "}
                        <Link className="font-semibold text-sky-500 hover:underline" href="/register">
                            Kayit ol
                        </Link>
                    </div>
                </section>
            </div>
        </main>
    );
};

export default LoginPage