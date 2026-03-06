"use client";
import Link from "next/link";
import { FC } from "react";
import { IconType } from "react-icons";

interface SidebarItemProps {
    label: string;
    href: string;
    icon: IconType;
    onClick?: () => void;
}
export const SidebarItem: FC<SidebarItemProps> = ({
    label,
    href,
    icon: Icon,
    onClick,
}) => {
    const content = (
        <div className="flex items-center">
            <div className="relative flex h-12 w-12 items-center justify-center rounded-full p-2 transition hover:bg-slate-300/10 lg:hidden">
                <Icon size={24} color="white" />
            </div>
            <div className="relative hidden items-center gap-4 rounded-full p-4 transition hover:bg-slate-300/10 lg:flex">
                <Icon size={24} color="white" />
                <p className="hidden text-xl text-white lg:block">{label}</p>
            </div>
        </div>
    );

    if (onClick) {
        return (
            <button
                type="button"
                onClick={onClick}
                className="flex items-center text-left"
            >
                {content}
            </button>
        );
    }

    return (
        <Link href={href} className="flex items-center">
            {content}
        </Link>
    );
};
