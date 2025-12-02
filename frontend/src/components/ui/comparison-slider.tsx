"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ComparisonSliderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const ComparisonSlider = React.forwardRef<HTMLDivElement, ComparisonSliderProps>(
  ({ className, children, ...props }, _ref) => {
    const [position, setPosition] = React.useState(50)
    const [isDragging, setIsDragging] = React.useState(false)
    const containerRef = React.useRef<HTMLDivElement>(null)
    const animationFrameRef = React.useRef<number | null>(null)
    const lastUpdateTimeRef = React.useRef<number>(0)

    const updatePosition = React.useCallback(
      (clientX: number) => {
        if (!containerRef.current) return

        const rect = containerRef.current.getBoundingClientRect()
        const x = clientX - rect.left
        const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100))
        
        // Throttle updates usando requestAnimationFrame para suavidad
        const now = performance.now()
        if (now - lastUpdateTimeRef.current >= 8) { // ~120fps máximo
          setPosition(percentage)
          lastUpdateTimeRef.current = now
        } else if (animationFrameRef.current === null) {
          animationFrameRef.current = requestAnimationFrame(() => {
            setPosition(percentage)
            lastUpdateTimeRef.current = performance.now()
            animationFrameRef.current = null
          })
        }
      },
      []
    )

    const handleMouseMove = React.useCallback(
      (e: MouseEvent) => {
        if (!isDragging) return
        updatePosition(e.clientX)
      },
      [isDragging, updatePosition]
    )

    const handleTouchMove = React.useCallback(
      (e: TouchEvent) => {
        if (!isDragging || e.touches.length === 0) return
        e.preventDefault()
        updatePosition(e.touches[0].clientX)
      },
      [isDragging, updatePosition]
    )

    const handleMouseDown = () => {
      setIsDragging(true)
    }

    const handleTouchStart = () => {
      setIsDragging(true)
    }

    const handleMouseUp = () => {
      setIsDragging(false)
    }

    const handleTouchEnd = () => {
      setIsDragging(false)
    }

    React.useEffect(() => {
      if (isDragging) {
        window.addEventListener("mousemove", handleMouseMove, { passive: true })
        window.addEventListener("mouseup", handleMouseUp)
        window.addEventListener("touchmove", handleTouchMove, { passive: false })
        window.addEventListener("touchend", handleTouchEnd)
        return () => {
          window.removeEventListener("mousemove", handleMouseMove)
          window.removeEventListener("mouseup", handleMouseUp)
          window.removeEventListener("touchmove", handleTouchMove)
          window.removeEventListener("touchend", handleTouchEnd)
          if (animationFrameRef.current !== null) {
            cancelAnimationFrame(animationFrameRef.current)
            animationFrameRef.current = null
          }
        }
      } else {
        // Cuando se suelta, cancelar cualquier animación pendiente
        if (animationFrameRef.current !== null) {
          cancelAnimationFrame(animationFrameRef.current)
          animationFrameRef.current = null
        }
      }
    }, [isDragging, handleMouseMove, handleTouchMove])

    const childrenArray = React.Children.toArray(children)
    const beforeChild = childrenArray.find(
      (child) => React.isValidElement(child) && child.type === ComparisonBefore
    )
    const afterChild = childrenArray.find(
      (child) => React.isValidElement(child) && child.type === ComparisonAfter
    )

    return (
      <div
        ref={containerRef}
        className={cn("relative h-full overflow-hidden rounded-lg select-none comparison-slider", className)}
        style={{ userSelect: 'none', WebkitUserSelect: 'none' }}
        {...props}
      >
        {beforeChild && (
          <div className="absolute top-0 left-0 h-full flex items-center justify-center" style={{ width: '100%' }}>{beforeChild}</div>
        )}
        {afterChild && (
          <div
            className="absolute top-0 left-0 h-full flex items-center justify-center"
            style={{ 
              width: '100%',
              clipPath: `inset(0 ${100 - position}% 0 0)`,
              transition: isDragging ? 'none' : 'clip-path 0.1s ease-out'
            }}
          >
            {afterChild}
          </div>
        )}
        <div
          className="absolute top-0 bottom-0 w-1 bg-[#55f3ff] cursor-ew-resize z-10 transition-all duration-200 ease-out touch-none select-none"
          style={{ 
            left: `${position}%`, 
            transform: "translateX(-50%)",
            transition: isDragging ? 'none' : 'left 0.1s ease-out',
            userSelect: 'none',
            WebkitUserSelect: 'none',
            outline: 'none'
          }}
          onMouseDown={handleMouseDown}
          onTouchStart={handleTouchStart}
          tabIndex={-1}
        >
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-[#55f3ff] border-2 border-white shadow-lg flex items-center justify-center">
            <div className="flex gap-0.5">
              <div className="w-0.5 h-3 bg-white rounded-full" />
              <div className="w-0.5 h-3 bg-white rounded-full" />
            </div>
          </div>
        </div>
      </div>
    )
  }
)
ComparisonSlider.displayName = "ComparisonSlider"

interface ComparisonBeforeProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const ComparisonBefore = React.forwardRef<HTMLDivElement, ComparisonBeforeProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div ref={ref} className={cn("h-full flex items-center justify-center", className)} {...props}>
        {children}
      </div>
    )
  }
)
ComparisonBefore.displayName = "ComparisonBefore"

interface ComparisonAfterProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const ComparisonAfter = React.forwardRef<HTMLDivElement, ComparisonAfterProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div ref={ref} className={cn("h-full flex items-center justify-center", className)} {...props}>
        {children}
      </div>
    )
  }
)
ComparisonAfter.displayName = "ComparisonAfter"

export { ComparisonSlider, ComparisonBefore, ComparisonAfter }

