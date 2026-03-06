"use client"

import { useFormik } from "formik";
import { useState, useEffect } from "react";
import { ProfilePhoto } from "../../Image/ProfilePhoto";
import { postRequest } from "./postRequest";
import { useRouter } from "next/navigation";


interface UserIdProp {
    userId: string
    photoUrl: string
    post?: ITweetProps
    mode: "Tweet" | "Cevap"
}
const SendPost: React.FC<UserIdProp> = ({ userId, photoUrl, mode, post }) => {

    const [body, setBody] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [disabled, setDisabled] = useState(true)

    const router = useRouter()

    useEffect(() => {
        setDisabled(body.trim() === "")
    }, [body]);


    const formik = useFormik({

        initialValues: {
            text: ""
        },

        onSubmit: async (values, { resetForm }) => {
            setIsLoading(true);
            try {
                await postRequest(body, post?.id ?? null)
                resetForm();
                setBody("");

            }
            catch (error) {
                throw error
            }
            finally {
                setIsLoading(false);
                router.refresh()
            }
        }
    });

    return (
        <form onSubmit={formik.handleSubmit}>
            <div className='border-b-[1px] border-neutral-800 px-5 py-2'>
                <div className='flex flex-row gap-4'>
                    <ProfilePhoto
                        ownerId={userId}
                        photo={photoUrl} />
                    <div className='w-full'>
                        <textarea
                            disabled={isLoading}
                            onChange={(e) => setBody(e.target.value)}
                            onSubmit={() => {
                                setBody("")
                            }}
                            value={body}
                            className='
                                        disabled:opacity-50
                                        peer
                                        resize-none
                                        mt-6
                                        w-full
                                        bg-black
                                        ring-0
                                        outline-none
                                        text-[20px]
                                        placeholder-neutral-500
                                        text-white'
                            placeholder={mode === "Tweet"
                                ? "What's Happening"
                                : "Send Answer"
                            }
                        ></textarea>

                        {mode === "Tweet"
                            && <hr className='
                        opacity-100
                        h-[1px]
                        w-full
                        border-neutral-800
                        transition' />}
                    </div>
                </div>
                {mode === "Tweet"
                    ?
                    <div className="mt-4  flex flex-row justify-end">
                        <button className={`bg-[#009CFF] rounded-3xl w-24 h-10 ${disabled ? "opacity-50" : "opacity-100"}`}
                            type="submit"
                            disabled={disabled || isLoading}> Gönder </button>
                    </div>
                    :
                    <div className="flex flex-row items-center justify-end">
                        <button className={`bg-[#009CFF] rounded-3xl w-24 h-10 ${disabled ? "opacity-50" : "opacity-100"}`}
                            type="submit"
                            disabled={disabled || isLoading}> Yanıtla </button>
                    </div>}

            </div>
        </form>
    )
}

export default SendPost