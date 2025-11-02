package sorting;

import java.util.Arrays;

/**
 * Time Complexity: O(n log n)
 * Auxiliary Space: O(log n), due to the recursive call stack. However, auxiliary space can be O(1) for iterative implementation.
 */
import java.util.Arrays;

public class HeapSort {
    public static void main(String[] args) {
        int arr[] = {9, 4, 33, 8, 11, 2, 5, 1, 16, 10, 22, 3, 7, 13, 19};
        heapSort(arr);
        System.out.println(Arrays.toString(arr));
    }

    static void heapSort(int[] arr) {
        // Build max heap
        for(int i= (arr.length/2 - 1) ; i >= 0; i--){
            maxHeapify(arr, i, arr.length);
        }

        // Extract and reheapify
        for(int size=arr.length-1; size>0; size--){
            swap(arr, size, 0);
            maxHeapify(arr, 0, size);
        }

    }

    static void maxHeapify(int[] arr, int rootIndex, int size) {
        int largest = rootIndex;

        int leftIndex = rootIndex * 2 + 1;
        if (leftIndex < size && arr[leftIndex] > arr[largest]) {
            largest = leftIndex;
        }

        int rightIndex = rootIndex * 2 + 2;
        if (rightIndex < size && arr[rightIndex] > arr[largest]) {
            largest = rightIndex;
        }

        if (largest != rootIndex) {
            swap(arr, largest, rootIndex);

            maxHeapify(arr, largest, size);
        }
    }

    static void swap(int[] arr, int l, int r) {
        int temp = arr[l];
        arr[l] = arr[r];
        arr[r] = temp;
    }
}