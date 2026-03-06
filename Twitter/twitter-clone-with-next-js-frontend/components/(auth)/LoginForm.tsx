"use client"

import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import { useRouter } from "next/navigation"

interface Values {
    email: string;
    password: string;
}

const validationSchema = Yup.object().shape({

    email: Yup.string().email('Geçersiz email formatı').required('Email gereklidir'),
    password: Yup.string().required('Şifre gereklidir'),
});

const LoginForm = () => {
    const router = useRouter()

    return (
        <Formik
            initialValues={{
                email: '',
                password: '',
            }}
            validationSchema={validationSchema}
            onSubmit={async (values) => {
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(values),
                    });

                    if (!response.ok) {
                        const data = await response.json().catch(() => null);
                        throw new Error(data?.detail || 'Giris basarisiz.');
                    }

                    toast.success('Giris basarili!');
                    router.push("/");
                } catch (error: any) {
                    toast.error(error?.message || 'Giris basarisiz.');
                }
            }}
        >
            {({ isSubmitting }) => (
                <Form className="grid gap-5">
                    <label htmlFor="email" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Email</p>
                        <Field
                            type="email"
                            name="email"
                            placeholder="Email"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        <ErrorMessage name="email" component="div" className="text-xs text-red-400" />
                    </label>
                    <label htmlFor="password" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Sifre</p>
                        <Field
                            type="password"
                            name="password"
                            placeholder="Sifre"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        <ErrorMessage name="password" component="div" className="text-xs text-red-400" />
                    </label>

                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="mt-2 w-full rounded-full bg-white px-4 py-3 text-sm font-bold text-black transition hover:bg-zinc-200 disabled:opacity-60"
                    >
                        {isSubmitting ? 'Giris yapiliyor...' : 'Giris yap'}
                    </button>
                </Form>
            )}
        </Formik>
    );
};

export default LoginForm;