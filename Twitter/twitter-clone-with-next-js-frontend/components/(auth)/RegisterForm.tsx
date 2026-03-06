"use client"

import { Form, Field, Formik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';

import { useRouter } from 'next/navigation';
import { signup } from '@/lib/auth';

interface Values {
    username: string;
    email: string;
    password: string;
}

const validationSchema = Yup.object().shape({
    username: Yup.string().required('Kullanıcı adı gereklidir'),
    email: Yup.string().email('Geçersiz email formatı').required('Email gereklidir'),
    password: Yup.string().min(8, 'Sifre en az 8 karakter olmali').required('Şifre gereklidir'),
    confirmPassword: Yup.string()
        .oneOf([Yup.ref('password')], 'Şifreler eşleşmiyor')
        .required('Şifre onayı gereklidir'),
});

const RegisterForm = () => {
    const router = useRouter();
    return (
        <Formik
            initialValues={{
                username: '',
                email: '',
                password: '',
                confirmPassword: ''
            }}
            validationSchema={validationSchema}
            onSubmit={async (values, { setSubmitting }) => {
                try {
                    await signup(values);
                    router.push("/login");
                } catch (error) {
                    console.error("Kayit sirasinda hata olustu.", error);
                } finally {
                    setSubmitting(false);
                }
            }}
        >
            {({ errors, touched, isSubmitting }) => (
                <Form className="grid gap-5">
                    <label htmlFor="username" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Kullanici adi</p>
                        <Field
                            type="text"
                            name="username"
                            placeholder="Kullanici adi"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        {errors.username && touched.username && (
                            <p className="text-xs text-red-400">{errors.username}</p>
                        )}
                    </label>
                    <label htmlFor="email" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Email</p>
                        <Field
                            type="email"
                            name="email"
                            placeholder="Email"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        {errors.email && touched.email && (
                            <p className="text-xs text-red-400">{errors.email}</p>
                        )}
                    </label>
                    <label htmlFor="password" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Sifre</p>
                        <Field
                            type="password"
                            name="password"
                            placeholder="Sifre"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        {errors.password && touched.password && (
                            <p className="text-xs text-red-400">{errors.password}</p>
                        )}
                    </label>
                    <label htmlFor="confirmPassword" className="grid gap-2">
                        <p className="text-sm font-semibold text-zinc-200">Sifre onayi</p>
                        <Field
                            type="password"
                            name="confirmPassword"
                            placeholder="Sifreyi tekrar gir"
                            className="w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 text-white placeholder-zinc-500 outline-none transition focus:border-sky-500"
                        />
                        {errors.confirmPassword && touched.confirmPassword && (
                            <p className="text-xs text-red-400">{errors.confirmPassword}</p>
                        )}
                    </label>
                    <button
                        className="mt-2 w-full rounded-full bg-white px-4 py-3 text-sm font-bold text-black transition hover:bg-zinc-200 disabled:opacity-60"
                        type="submit"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Kayit olusturuluyor...' : 'Kayit ol'}
                    </button>
                </Form>
            )}
        </Formik>
    );
};

export default RegisterForm;